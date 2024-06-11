
from enum import Enum
from json import JSONDecoder, JSONEncoder
from operator import contains
import os
from typing import Union
from datetime import datetime
from genericpath import exists
import glob
from time import sleep
from RPi import GPIO
from picamera2 import Picamera2
from src.mq2 import MQ2
from src.web import NodeWebClient
from src.logger import Logger
from src.sensor import CameraSensor, FileOutputSensor, OutputSensor, MultiOutputSensor, InputSensor, Sensor, SensorType
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# GPIO Pins
# The GPIO pins used for the different sensors
TEMP_PIN = 4
BUZZER_PIN = 24
GAS_SMOKE_PIN = 17

# Critical values
# when this value is reached, the alarm will turn on
CRITICAL_TEMP    = 30          # in degrees celsius
CRITICAL_CO      = 200         # PPM of the gas in the air
CRITICAL_H2      = 200         # PPM of the gas in the air
CRITICAL_CH4     = 200         # PPM of the gas in the air
CRITICAL_LPG     = 200         # PPM of the gas in the air
CRITICAL_PROPANE = 200         # PPM of the gas in the air
CRITICAL_ALCOHOL = 200         # PPM of the gas in the air
CRITICAL_SMOKE   = 200         # PPM of the gas in the air       
# https://www.co2meter.com/blogs/news/carbon-dioxide-indoor-levels-chart

# Priority levels
# With a higher priority level, the measured values can cause the alarm to trigger earlier before the critical temperature is reached.
# This will only occure if multiple sensors are reaching their critical level
PRIORITY_TEMP    = 1
PRIORITY_CO      = 3
PRIORITY_H2      = 2
PRIORITY_CH4     = 2
PRIORITY_LPG     = 2
PRIORITY_PROPANE = 2
PRIORITY_ALCOHOL = 2
PRIORITY_SMOKE   = 3

# Amount of decimals the gas values are rounded (co, h2, ch4, lpg, propane, alcohol and smoke)
GAS_ROUNDING = 3

# This is the calibration value used for the sensor, 
# change to 0 if it has te be determined in each startup
GAS_CALIBRATION = 7810.727510362364
# This is the time in seconds a calibration will take, 
# a longer time will give better results, but it makes the node unusable
# Only used when GAS_CALIBRATION is 0
GAS_CALIBRATION_TIME = 20

# Frequency of the buzzer tone
BUZZ_FREQ = 500
# Duty Cycle of the buzzer
BUZZ_DC = 50

# DO NOT CHANGE ANYTHING BELOW THIS COMMENT
PATH = os.getcwd()
DEVICE_PATH = "/sys/bus/w1/devices/"
LOG_PATH = PATH+"/logs/"
RECORDING_PATH = PATH+"/recordings/"
DATA_PATH = PATH+"/data/"

class Node():
    def __init__(self, logger: Logger):
        self.logger = logger
        self.alarm = Alarm(self)
        self.sensors: dict[SensorType, Sensor] = dict()
    
    def addSensor(self, sensor: Sensor):
        self.sensors[sensor.sensorType] = sensor

    def getSensor(self, type: SensorType) -> Union[Sensor, None]:
        return self.sensors.get(type)

    def getInputSensor(self, type: SensorType) -> Union[InputSensor, None]:
        sensor = self.sensors.get(type)
        if isinstance(sensor, InputSensor):
            return sensor
        return None

    def getOutputSensor(self, type: SensorType) -> Union[OutputSensor, None]:
        sensor = self.sensors.get(type)
        if isinstance(sensor, OutputSensor):
            return sensor
        return None
    
    def getFileOutputSensor(self, type: SensorType) -> Union[FileOutputSensor, None]:
        sensor = self.sensors.get(type)
        if isinstance(sensor, FileOutputSensor):
            return sensor
        return None
    
    def getMultiOutputSensor(self, type: SensorType) -> Union[MultiOutputSensor, None]:
        sensor = self.sensors.get(type)
        if isinstance(sensor, MultiOutputSensor):
            return sensor
        return None
    
    def encodeData(self) -> dict:
        data = dict()
        for sType in self.sensors:
            sensor = node.sensors[sType]
            if isinstance(sensor, OutputSensor): 
                data[sType.value] = sensor.data
            if isinstance(sensor, MultiOutputSensor):
                for subType in sensor.sensors:
                    data[subType.value] = sensor.sensors[subType].data
        return data


    def encode(self) -> dict:
        return {
            "time": datetime.now().timestamp(),
            "alarm": self.alarm.encode(),
            "data": self.encodeData()
        }

class AlarmStatus(Enum):
    SAFE = 0
    WARNING = 1
    CRITICAL = 2

    def getApiStatus(self) -> bool:
        return self == AlarmStatus.CRITICAL

class Alarm():
    def __init__(self, node: Node):
        self.status = AlarmStatus.SAFE
        self.sensorPriority: dict[SensorType, float] = dict()
        self.node = node


    def update(self):
        lastStatus = self.status
        priority = 0
        self.criticalSensors = []
        
        for sensorType in self.node.sensors:
            sensor = self.node.sensors[sensorType]
            if sensor.isDisabled(): continue

            if isinstance(sensor, OutputSensor):
                priority += self.sensorUpdate(sensor)
            elif isinstance(sensor, MultiOutputSensor):
                for subSensorType in sensor.sensors: # type: ignore
                    priority += self.sensorUpdate(sensor.sensors[subSensorType])

        # Set status of the sensor alarm
        if priority < 1: self.status = AlarmStatus.SAFE
        elif priority < 2: self.status = AlarmStatus.WARNING
        else: self.status = AlarmStatus.CRITICAL

        # Get the alarm status of the server
        serverAlarm = getServerStatus().get("alertStatus")
        serverAlarmStatus = AlarmStatus.SAFE
        if serverAlarm != None and serverAlarm: 
            serverAlarmStatus = AlarmStatus.CRITICAL

        # If the alarm level of the server is higher then our own, update it to the servers level
        if self.status.value < serverAlarmStatus.value: self.status = serverAlarmStatus

        if lastStatus != self.status: self.onChange()
        return self.status
    
    def onChange(self):
        
        if self.status == AlarmStatus.SAFE: 
            self.node.logger.info("All levels are back to normal, the alarm is turned off")
        elif self.status == AlarmStatus.WARNING: 
            self.node.logger.warning("High levels have been detected, the alarm is turned off")
            self.node.logger.warning("Alarm: " + JSONEncoder().encode(self.encode()))
        elif self.status == AlarmStatus.CRITICAL: 
            self.node.logger.emergency("Critical level shave been detected, the alarm has turned on")
            self.node.logger.emergency("Alarm: " + JSONEncoder().encode(self.encode()))

        for sensorType in self.node.sensors:
            sensor = self.node.sensors[sensorType]
            if not isinstance(sensor, InputSensor): continue

            if self.status == AlarmStatus.CRITICAL:
                sensor.start()
            else:
                try:
                    sensor.stop()
                except Exception as e:
                    self.node.logger.debug(str(e))
    
    def sensorUpdate(self, sensor: OutputSensor):
        priority = sensor.getAlarmPriority()
        if priority > 0:
            self.sensorPriority[sensor.sensorType] = priority
        return priority

    def encode(self) -> dict:
        encoded = {
            "alertStatus": self.status.getApiStatus(),
        }

        # for sensorType in self.sensorPriority:
        #     encoded["activeSensors"][sensorType.value] = self.sensorPriority[sensorType]

        return encoded

def start():
    '''
    Start the node application
    '''
    global node, webClient

    # create directories
    try:
        if not exists(LOG_PATH): os.mkdir(LOG_PATH, 0o777)
        if not exists(RECORDING_PATH): os.mkdir(RECORDING_PATH, 0o777)
        if not exists(DATA_PATH): os.mkdir(DATA_PATH, 0o777)
    except:
        print("Cannot start the system: cannot create required directories")
        exit()

    node = Node(Logger(LOG_PATH))

    node.logger.info("Initializing sensors...")
      
    GPIO.setmode(GPIO.BCM) # type: ignore

    initTempSensor()
    initGasSmokeSensor()
    initCamera()
    initBuzzer()
    
    node.logger.info("Starting the web client...")
    webClient = NodeWebClient(node.logger, DATA_PATH)
    webClient.start()
    
    node.logger.info("Finished Initialization")

    try:
        while True:

            update()

            sleep(1)
    except KeyboardInterrupt:
        shutdown()

def update():
    global node
    updateTemperature()
    updateGasSmoke()
    node.alarm.update()

    jsonData = JSONEncoder().encode(node.encode())
    node.logger.debug(jsonData)

    # store current data
    file = open(DATA_PATH+"node.json", "w+")
    file.write(jsonData)
    file.close()

def initGasSmokeSensor():
    global node, gasDetection
    sensor = MultiOutputSensor(SensorType.GAS)
    node.addSensor(sensor)

    sensor.add(OutputSensor(SensorType.CO, CRITICAL_CO, PRIORITY_CO))
    sensor.add(OutputSensor(SensorType.H2, CRITICAL_H2, PRIORITY_H2))
    sensor.add(OutputSensor(SensorType.CH4, CRITICAL_CH4, PRIORITY_CH4))
    sensor.add(OutputSensor(SensorType.LPG, CRITICAL_LPG, PRIORITY_LPG))
    sensor.add(OutputSensor(SensorType.PROPANE, CRITICAL_PROPANE, PRIORITY_PROPANE))
    sensor.add(OutputSensor(SensorType.ALCOHOL, CRITICAL_ALCOHOL, PRIORITY_ALCOHOL))
    sensor.add(OutputSensor(SensorType.SMOKE, CRITICAL_SMOKE, PRIORITY_SMOKE))

    GPIO.setup(GAS_SMOKE_PIN, GPIO.IN) # type: ignore
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    ads.gain = 2/3
    # Create single-ended input on channels
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)
    
    try:

        gasDetection = MQ2(chan0, GAS_CALIBRATION)
        if not gasDetection.calibrated:
            node.logger.warning("The gas sensor is not calibrated!")            
            node.logger.info("Calibrating the gas sensor, this will take "+str(GAS_CALIBRATION_TIME)+" seconds")
            gasDetection.calibrate(GAS_CALIBRATION_TIME)
            node.logger.info("Calibration successful, GAS_CALIBRATION=" + str(gasDetection.r0))
    except ValueError:
        node.logger.warning("Gas sensor not found")
        askForShutdown()
        sensor.disable()
 

def updateGasSmoke():
    global node, gasDetection
    sensor = node.getMultiOutputSensor(SensorType.GAS)
    if sensor == None or sensor.isDisabled(): return

    try:
        gasDetection.measure()

        co = sensor.get(SensorType.CO)
        h2 = sensor.get(SensorType.H2)
        ch4 = sensor.get(SensorType.CH4)
        lpg = sensor.get(SensorType.LPG)
        propane = sensor.get(SensorType.PROPANE)
        alcohol = sensor.get(SensorType.ALCOHOL)
        smoke = sensor.get(SensorType.SMOKE)

        if co != None: co.data = round(gasDetection.getCO(), GAS_ROUNDING)
        if h2 != None: h2.data = round(gasDetection.getH2(), GAS_ROUNDING)
        if ch4 != None: ch4.data = round(gasDetection.getCH4(), GAS_ROUNDING)
        if lpg != None: lpg.data = round(gasDetection.getLPG(), GAS_ROUNDING)
        if propane != None: propane.data = round(gasDetection.getPropane(), GAS_ROUNDING)
        if alcohol != None: alcohol.data = round(gasDetection.getAlcohol(), GAS_ROUNDING)
        if smoke != None: smoke.data = round(gasDetection.getSmoke(), GAS_ROUNDING)

        # The digital value is reached, trigger the alarm
        if GPIO.input(GAS_SMOKE_PIN) == GPIO.LOW: # type: ignore
            if smoke != None: smoke.data = CRITICAL_SMOKE

    except IndexError:
        node.logger.error("Gas sensor not found, the sensor is now disabled.")
        sensor.disable()


def initTempSensor():
    global node
    sensor = FileOutputSensor(SensorType.TEMPERATURE, "", CRITICAL_TEMP, PRIORITY_TEMP)
    node.addSensor(sensor)

    GPIO.setup(TEMP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # type: ignore

    try:
        temp_folder = glob.glob(DEVICE_PATH + '28*')[0]
        sensor.file = temp_folder + '/w1_slave'

        return
        
    except IndexError:
        node.logger.error("Temperature sensor not found, the sensor is now disabled.")
        askForShutdown()
        sensor.disable()
    

def updateTemperature():
    global node
    sensor = node.getFileOutputSensor(SensorType.TEMPERATURE)
    if sensor == None or sensor.isDisabled(): return

    try:
        lines = sensor.getFileData()
        equals_pos = lines[1].find('t=')
    except (OSError, IndexError):
        node.logger.error("Cannot find the temperature sensor")
        sensor.disable()
        return

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        sensor.data = temp_c
    

def initBuzzer():
    global node
    sensor = InputSensor(SensorType.BUZZER, onStart=lambda: buzzerPwm.start(BUZZ_DC), onStop=lambda: buzzerPwm.stop())
    node.addSensor(sensor)

    GPIO.setup(BUZZER_PIN, GPIO.OUT) # type: ignore

    global buzzerPwm
    buzzerPwm = GPIO.PWM(BUZZER_PIN, BUZZ_FREQ) # type: ignore

def initCamera():
    global node

    try:
        camera = Picamera2()
        camera.close()
        sensor = CameraSensor(SensorType.CAMERA, node.logger)
        node.addSensor(sensor)

    except RuntimeError as err:
        node.logger.warning("Camera not found: " + str(err))
        askForShutdown()

def askForShutdown():
    enable = None
    while not contains(["y", "yes", "n", "no"], enable):
        enable = str(input("Do you want to shutdown the system? [y/n] ")).lower()

    if enable == "y" or enable == "yes":
        shutdown()

def shutdown():
    global node, webClient

    node.logger.info("Shuttingdown the web client")
    webClient.join()

    node.logger.info("Shuttingdown the sensors")

    # handle shutdown for all sensors
    for s in node.sensors:
        sensor = node.sensors[s]
        if isinstance(sensor, InputSensor):
            sensor.stop()

    GPIO.cleanup() # type: ignore

    node.logger.info("Shutdown successful, bye!")
    exit()

def getServerStatus():
    try:
        file = open(DATA_PATH + "server.json", "r")
        data = JSONDecoder().decode(file.read())
        file.close()

        return data
    except:
        return {}