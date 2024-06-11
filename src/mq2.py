from math import log10
from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

VC = 5 # Supply voltage
RL = 1500 # Load resistance
AIR_RATIO = 9.8 # RS/R0 of air

class MQ2:

    def __init__(self, channel: AnalogIn, r0: float = 0):
        
        self.channel = channel
        self.ratio = 0
        self.r0 = r0

        self.calibrated = r0 > 0


    def getRS(self, voltage: float):
        '''Calculate the resistance from the given voltage'''
        return (VC/voltage-1)*RL


    def getPPM(self, a: float, b: float):
        '''Calculate the PPM of the given ratio and a and b'''
        return pow(10, (log10(self.ratio) - b) / a)

    def getCO(self):
        # y0= 5.1 , y1= 1.5
        a = -0.313
        b = 1.427
        return self.getPPM(a, b)

    def getSmoke(self):
        # y0= 3.5 , y1= 0.6
        a = -0.451
        b = 1.581
        return self.getPPM(a, b)

    def getCH4(self):
        # y0= 3.0 , y1= 0.7
        a = -0.372
        b = 1.333
        return self.getPPM(a, b)

    def getAlcohol(self):
        # y0= 2.9 , y1= 0.55
        a = -0.425
        b = 1.44
        return self.getPPM(a, b)

    def getH2(self):
        # y0= 2.1 , y1= 0.33
        a = -0.473
        b = 1.411
        return self.getPPM(a, b)

    def getPropane(self):
        # y0= 1.7 , y1= 0.28
        a = -0.461
        b = 1.291
        return self.getPPM(a, b)

    def getLPG(self):
        # y0= 1.6 , y1= 0.27
        a = -0.455
        b = 1.251
        return self.getPPM(a, b)


    def calibrate(self, time: int = 60):
        '''
        Calibrate the sensor
        time=The amount of seconds for the calibration, a higher value is better
        '''
        value = 0
        i = 0
        while i < time*2:
            value += self.channel.voltage
            sleep(0.5)
            i += 1

        avgValue = value / i
        voltage = (avgValue * VC) / 5

        rs = self.getRS(voltage)

        self.r0 = rs/AIR_RATIO
        self.calibrated = True

    def measure(self):
        '''Measure the current resistance'''
        voltage = self.channel.voltage
        rs = self.getRS(voltage)
        self.ratio = rs/self.r0
    