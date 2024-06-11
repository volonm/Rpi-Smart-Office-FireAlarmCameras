import requests

HTTP_SERVER_ADDRESS = "http://172.20.10.2:8000"
POST_TURN_OFF_ALARM = "/sensors/stopAlert"

headers = {"Content-Type": "application/json"}
body = {}

try:
    res = requests.post(HTTP_SERVER_ADDRESS + POST_TURN_OFF_ALARM, json=body, headers=headers)
    print("The alarm has turned off")
    print("Status: ", res.status_code)
except:
    print("Something went wrong")