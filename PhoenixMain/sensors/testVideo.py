import requests

api_url = "http://172.20.10.2:8000/sensors/uploadVideo"
video_file_path = ("C:/UT/war/fpv/855.mp4")

# Define the title field
data = {'rid': 1}

files = {'video_file': open(video_file_path, 'rb')}

print(files)

response = requests.post(api_url, data=data, files=files)

if response.status_code == 201:
    print("Video uploaded successfully")
else:
    print(f"Failed to upload video. Status code: {response.status_code}")
    print(response.text)
