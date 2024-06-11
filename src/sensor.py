
from enum import Enum
import io
from src.logger import Logger
from time import time_ns
from typing import Callable, Union
from datetime import datetime
from circuitpython_typing import ReadableBuffer
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, FileOutput
from threading import Condition, Event, Thread
from src.web import NodeWebClient

class SensorType(Enum):
    GAS = "GAS"
    BUZZER = "BUZZER"
    CAMERA = "CAMERA"


    TEMPERATURE = "TEMP"
    CO = "CO"
    H2 = "H2"
    CH4 = "CH4"
    LPG = "LPG"
    PROPANE = "PROPANE"
    ALCOHOL = "ALCOHOL"
    SMOKE = "SMOKE"


    def __str__(self) -> str:
        return self.value
    

class SensorStatus(Enum):
    DISABLED = 0
    ENABLED = 1
    OFF = 2
    ON = 3



class Sensor():
    '''
    A default sensor
    '''
    def __init__(self, sensorType: SensorType, status: SensorStatus):
        self.sensorType: SensorType = sensorType
        self.status: SensorStatus = status

    def isDisabled(self):
        '''
        Get if the sensor is disabled
        '''
        return self.status == SensorStatus.DISABLED

    def disable(self):
        '''
        Mark the sensor as disabled
        '''
        self.status = SensorStatus.DISABLED

    def setStatus(self, status: SensorStatus):
        '''
        Sets the status of the sensor
        '''
        self.status = status
    
    def encode(self) -> dict:
        return {
            "STATUS": self.status.value
        }

class InputSensor(Sensor):
    '''
    A sensor that requires an input to do something
    The sensor triggers on the specified alarm status
    '''

    def __init__(self, sensorType: SensorType, onStart: Callable, onStop: Callable):
        super().__init__(sensorType, SensorStatus.OFF)
        self.onStart = onStart
        self.onStop = onStop

    def start(self):
        '''
        Changes the sensor status to on.
        returns true if the status is changed, false otherwise
        '''
        if self.status == SensorStatus.OFF:
            self.status = SensorStatus.ON
            self.onStart()
            return True

        return False
    
    def stop(self):
        '''
        Changes the sensor status to off
        returns true if the status is changed, false otherwise
        '''

        if self.status == SensorStatus.ON:
            self.status = SensorStatus.OFF
            self.onStop()
            return True

        return False
    
    def isStarted(self):
        '''
        Get if the sensor is on
        '''
        return self.status == SensorStatus.ON

class OutputSensor(Sensor):
    '''
    A sensor that outputs data
    '''
    def __init__(self, sensorType: SensorType, critical: float, priority: int = 1):
        super().__init__(sensorType, SensorStatus.ENABLED)
        self.data: float = 0
        self.critical: float = critical
        self.priority: int = priority

        # The warning level is determined by the critical and priority level and represents a lower threshold.
        # When this threshold is reached, the sensor will be added to the alarm sensors including a low alarm priority level
        # this makes fires faster to regocnize when not all sensors have reached the critical level
        self.warning: float = self.critical - self.critical*((self.priority)/10)
    
    def getAlarmPriority(self) -> int:
        if self.reachedCritical(): return 2
        elif self.reachedWarning(): return 1
        else: return 0
    
    def encode(self) -> dict:
        encoded = super().encode()
        encoded["DATA"] = self.data
        return encoded
    
    def reachedCritical(self):
        return self.data >= self.critical
    
    def reachedWarning(self):
        return self.data >= self.warning 
    
class FileOutputSensor(OutputSensor):
    def __init__(self, sensorType: SensorType, file: str, critical: float, priority: int = 1):
        super().__init__(sensorType, critical, priority)
        self.file = file

    def getFileData(self):
        file = open(self.file, "r")
        lines = file.readlines()
        file.close()
        return lines

class MultiOutputSensor(Sensor):
    '''
    A data sensor that produces multiple types of data
    '''
    def __init__(self, sensorType: SensorType):
        super().__init__(sensorType, SensorStatus.ENABLED)

        self.sensors: dict[SensorType, OutputSensor] = dict()

    def add(self, sensor: OutputSensor):
        self.sensors[sensor.sensorType] = sensor
    
    def get(self, sensorType: SensorType):
        return self.sensors.get(sensorType)
    
    def encode(self) -> dict:
        encoded = super().encode()
        encoded["DATA"] = dict()
        for sensorType in self.sensors:
            encoded["DATA"][sensorType.value] = self.sensors[sensorType].data

        return encoded

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class CameraSensor(InputSensor):
    def __init__(self, sensorType: SensorType, logger: Logger):
        super().__init__(sensorType, self.onStart, self.onStop)
        self.stream: Union[Thread, None] = None
        self.event: Event = Event()
        self.logger = logger
        

    def onStart(self):
        self.event.clear()
        self.stream = Thread(target=self.handleCamera, args=[self.event, self.logger], daemon=True)
        self.stream.start()

    def onStop(self):
        if self.stream != None and self.stream.native_id != None: 
            self.event.set()
    
    @staticmethod
    def handleCamera(event: Event, logger: Logger):
        camera = Picamera2()

        streamOutput = StreamingOutput()

        # Get the output file
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # create the output
        encoder = H264Encoder()
        encoder.output = [FileOutput(streamOutput)]
        camera.encoders = encoder

        
        # start the camera
        camera.start()
        camera.start_encoder()
        logger.info("The camera is started")

        webRequests: list[Thread] = []
        cycle = 0
        liveFile = "recordings/" + time + "_"+str(cycle)+".mp4"
        liveFileOutput = FfmpegOutput(liveFile)
        liveFileOutput.start()
        startRecording = time_ns()//1000000
        try:
            while not event.is_set():
                with streamOutput.condition:
                    streamOutput.condition.wait()
                    frame: ReadableBuffer = streamOutput.frame

                    if frame != None:
                        liveFileOutput.outputframe(frame)

                currentTime = time_ns()//1000000
                if currentTime - startRecording > 20000:
                    liveFileOutput.stop()

                    t = Thread(target=NodeWebClient.sendMp4File, args=[liveFile], daemon=True)
                    t.start()
                    webRequests.append(t)
                    
                    cycle += 1
                    liveFile = "recordings/" + time + "_"+str(cycle)+".mp4"
                    liveFileOutput = FfmpegOutput(liveFile)
                    liveFileOutput.start()
                    startRecording = currentTime

        finally:
            liveFileOutput.stop()
            camera.stop_encoder()
            camera.close()
            logger.info("The camera has stopped")

    
