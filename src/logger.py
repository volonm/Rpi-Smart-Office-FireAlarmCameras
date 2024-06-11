from enum import Enum
from datetime import datetime
from genericpath import exists
from os import mkdir

DAY_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S.%f"
LOG_FORMAT = DAY_FORMAT + " " + TIME_FORMAT

class LogStatus(Enum):
    INFO = "Info"
    ERROR = "Error"
    WARNING = "Warning"
    EMERGENCY = "Emergency"
    DEBUG = "Debug"

class Logger():

    def __init__(self, logPath: str):
        self.path = logPath
        # make sure it ends with a /
        if not self.path.endswith("/"): self.path += "/"

        if not exists(self.path):
            mkdir(self.path)

    def log(self, status: LogStatus, msg: str, printLine: bool = True):
        date = datetime.now()
        today = date.strftime(DAY_FORMAT)
        time = date.strftime(LOG_FORMAT)
        log = "[" + time + "] [" + status.value + "] " + msg
        if printLine: print(log)

        file = open(self.path + today + ".log", "a+")
        file.write(log + "\n")
        file.close()
    
    def info(self, msg: str):
        '''Called to inform the user'''
        self.log(LogStatus.INFO, msg)
    
    def error(self, msg: str):
        '''Called when an error occured'''
        self.log(LogStatus.ERROR, msg)
    
    def warning(self, msg: str):
        '''Called when there happend something unexpected '''
        self.log(LogStatus.WARNING, msg)
    
    def emergency(self, msg: str):
        '''Called when the program is not able to recover from an error'''
        self.log(LogStatus.EMERGENCY, msg)

    def debug(self, msg: str, printLine = False):
        '''Called when the program wants to log data that is not visible in the console'''
        self.log(LogStatus.DEBUG, msg, printLine)
