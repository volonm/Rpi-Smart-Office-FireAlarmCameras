import requests

HTTP_SERVER_ADDRESS = "http://172.20.10.2:8000"
POST_TURN_ON_ALARM = "/sensors/systemAlarm"

headers = {"Content-Type": "application/json"}
body = {
    "rid": 1,
    "alertStatus": True
}

try:
    res = requests.post(HTTP_SERVER_ADDRESS + POST_TURN_ON_ALARM, json=body, headers=headers)
    print("The alarm has turned on")
    print("Status: ", res.status_code)
except:
    print("Something went wrong")