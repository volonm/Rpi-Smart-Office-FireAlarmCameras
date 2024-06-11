

from json import JSONDecoder, JSONEncoder
from os import kill
from signal import SIGINT
from threading import Event, Thread
from time import sleep
import requests
from src.logger import Logger

# server address
HTTP_SERVER_ADDRESS = "http://172.20.10.2:8000"

# DO NOT CHANGE ANYTHING BELOW THIS COMMENT

# URL paths
POST_NODE_DATA_PATH = "/sensors/sensorData"
POST_ALARM_STATUS_PATH = "/sensors/systemAlarm"
GET_SERVER_DATA_PATH = "/sensors/getSysStatus"
POST_CREATE_ENTRY = "/sensors/createSensorEntry"
POST_UPLOAD_VIDEO = "/sensors/uploadVideo"

# Key to identify this node by the server
SECRET_KEY = "TRFAMuEiNzxUUaskISKiICSRL3r8rfQV" 

# After how many seconds we should check for updates on the server
GET_SERVER_DATA_TIME  = 10
# After how many seconds we should send our data
POST_NODE_DATA_TIME = 5
# After how many seconds we should send our data when the alarm is triggered
POST_ALARM_STATUS_TIME = 1
# Time a request is allowed to take before it is shutdown
TIMEOUT = 5


class NodeWebClient(Thread):

    def __init__(self, logger: Logger, dataPath: str):
        super().__init__()
        self.logger = logger
        self.dataPath = dataPath
        self.processes: list[Thread] = []
        self.nodeData = {}
        self.joined = False
        self.connectionEvent = Event()

    def makeConnection(self):
        data = {"key": SECRET_KEY}
        
        try:
            res = requests.post(HTTP_SERVER_ADDRESS + POST_CREATE_ENTRY, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)
        except:
            self.logger.debug("Cannot connect to the server, retrying...")
            self.connectionEvent.clear()
            return
            
        f = open(self.dataPath + "auth.json", "w+")
        f.write(res.content.decode())
        f.close()

        self.connectionEvent.set()
        self.logger.info("Connected to the server")

    def run(self):
        auth = {}
        self.logger.info("Connecting to the server...")

        count = 0
        while self.is_alive() and not self.joined:
            # Not connected
            if not self.connectionEvent.is_set():
                self.makeConnection()
                auth = self.getAuthData()
                sleep(1)
                continue

            lastAlarm = self.nodeData.get("alarm")
            if lastAlarm == None: lastAlarm = {"alertStatus": False}

            self.getNodeData()

            data = self.nodeData.get("data")
            alarm = self.nodeData.get("alarm")
            
            if alarm != None and alarm["alertStatus"] != lastAlarm["alertStatus"]:
                self.logger.debug("Send alarm status to the server")
                self.startThread(Thread(target=self.postData, args=[POST_ALARM_STATUS_PATH, alarm, auth], daemon=True))

            if count % GET_SERVER_DATA_TIME == 0:
                self.logger.debug("Get data from the server")
                self.startThread(Thread(target=self.requestServerData, args=[GET_SERVER_DATA_PATH, self.dataPath + "server.json", auth], daemon=True))
            
            if data != None and (count % POST_NODE_DATA_TIME == 0 or (alarm != None and alarm.get("alarmStatus") == True and count % POST_ALARM_STATUS_TIME == 0)):
                self.logger.debug("Send data to the server")
                self.startThread(Thread(target=self.postData, args=[POST_NODE_DATA_PATH, data, auth], daemon=True))

            sleep(1)
            count += 1

        self.logger.info("Stopping all running web requests...")
        self.killProcesses()

    def killProcesses(self):
        for p in self.processes:
            pid = p.native_id
            if pid == None: continue

            try:
                kill(pid, SIGINT)
            except ProcessLookupError: 
                pass

    def startThread(self, process: Thread):
        self.processes.append(process)
        process.start()

    def getNodeData(self):
        
        try:
            file = open(self.dataPath + "node.json", "r")
            lines = file.read()
            if len(lines) > 0: self.nodeData = JSONDecoder().decode(lines)
            file.close()
        except FileNotFoundError:
            self.nodeData = {}
        
    def join(self, timeout = None) -> None:
        self.joined = True
        return super().join(timeout)
    
    @staticmethod
    def getAuthData():
        try:
            f = open("data/auth.json", "r")
            data = JSONDecoder().decode(f.read())
            f.close()
            return data
        except:
            return None


    @staticmethod
    def requestServerData(path: str, fileName: str, auth: dict):
        headers = {"Authorization": "Token " + str(auth.get("token"))}
        data = {}
        try:
            res = requests.get(HTTP_SERVER_ADDRESS + path, timeout=TIMEOUT, headers=headers)
            data = JSONDecoder().decode(res.content.decode())
        except:
            pass

        file = open(fileName, "w+")
        file.write(JSONEncoder().encode(data))
        file.close()

    @staticmethod
    def postData(path: str, data: dict, auth: dict):
        data["rid"] = auth.get("id")
        headers = {"Content-Type": "application/json", "Authorization": "Token " + str(auth.get("token"))}
        try:
            requests.post(HTTP_SERVER_ADDRESS + path, data=JSONEncoder().encode(data), headers=headers, timeout=TIMEOUT)    
        except:
            pass

    @staticmethod  
    def sendMp4File(filePath: str):
        auth = NodeWebClient.getAuthData()
        if auth == None: return

        headers = {"Authorization": "Token " + str(auth.get("token"))}
        data = {"rid": auth.get("id")}
        try:
            files = {"video_file": open(filePath, "rb")}
            res = requests.post(HTTP_SERVER_ADDRESS + POST_UPLOAD_VIDEO, data=data, files=files,headers=headers, timeout=TIMEOUT)
            print(res)
        except:
            pass

