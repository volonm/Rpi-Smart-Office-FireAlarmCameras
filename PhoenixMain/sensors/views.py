import os
import secrets
import string
from authorization.decorators import only_rasps
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from PhoenixMain import settings
from .models import Raspberry
from .models import Recording
from authorization.decorators import only_rasps, session_valid
from .models import SensorData
from .models import SystemAlertLog
from email.message import EmailMessage
import smtplib
import string
import ssl
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import SystemStatus
from .serializers import SensorDataSerializer, VideoSerializer, VideoUploadSerializer, SystemAlertLogSerializer

# Create your views here.

# SECRET KEY TO IDENTIFY NEW PI
SECRET_KEY = "TRFAMuEiNzxUUaskISKiICSRL3r8rfQV"

# Email System
emailSender = 'phoenix.firealarm@gmail.com'
emailPassword = 'lgej jkke dwsc ekfr'

body = ("Welcome our Favourite Client"
        "\nThe Alarm is being triggered now in the room: ")


# Api to receives json with sensor
@api_view(['POST'])
@only_rasps
def receiveSensorData(request):
    serializer = SensorDataSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=200)

    else:
        return Response(status=403)


# api to update system status(alert status )
@api_view(['POST'])
@only_rasps
def alertStatus(request):
    currentSystemStatus = SystemStatus.objects.get(id=1).status
    sensorStatus = request.data["alertStatus"]
    rid = request.data["rid"]
    if currentSystemStatus:
        return Response(status=200)
    elif sensorStatus and not currentSystemStatus:
        initSystemAlert(rid)
        room = Raspberry.objects.get(id=rid).name
        init_sending_emails(room)
        return Response(status=200)

    else:
        return Response(status=200)


# api to get current system status
@api_view(['GET'])
def getSysStatus(request):
    currentSystemStatus = SystemStatus.objects.get(pk=1)
    return Response({"alertStatus": currentSystemStatus.status}, status=200)


# api to stop aller
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def stopAlert(request):
    currentSystemStatus = SystemStatus.objects.get(pk=1)
    currentSystemStatus.status = False
    currentSystemStatus.save()
    logEntry = SystemAlertLog(rid=-1, msg="Alert stopped")
    logEntry.save()
    return Response(status=200)


# api to register rsp in system and provide token and its id in response
@api_view(['POST'])
def createSensorEntry(request):
    key = request.data['key']
    if key:
        if key == SECRET_KEY:
            name = "Undefined"
            token = genSensorToken(32)
            instance = Raspberry(name=name, token=token)
            instance.save()
            return Response({"token": token, "id": instance.pk}, status=200)

    else:
        return Response(status=406)


def genSensorToken(len):
    token_characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(token_characters) for _ in range(len))
    return token


def initSystemAlert(rid):
    print("System ALERT")
    currentSystemStatus = SystemStatus.objects.get(id=1)
    currentSystemStatus.status = True
    currentSystemStatus.save()
    roomName = Raspberry.objects.get(id=rid).name
    logEntry = SystemAlertLog(rid=rid, msg=f"Alert started in {roomName}")
    logEntry.save()
    # thread = Thread(call_command('sync_videos_until_alert_stops'))
    # thread.start()
    print("lets see")
    # call_command('sync_all_apps') #call my custom sync command
    # call_command('sync_videos_until_alert_stops')


# api to receive videos from sensor rsp
@api_view(['POST'])
@only_rasps
def uploadVideo(request):
    serializer = VideoUploadSerializer(data=request.data)
    if serializer.is_valid():
        video_file = serializer.validated_data['video_file']
        rid = serializer.validated_data['rid']
        raspberry = Raspberry.objects.get(pk=rid)
        # Create a new Video object and save the uploaded video file
        video = Recording(rid=raspberry, file=video_file)
        video.save()

        return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# provides with the file  path to requested video
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def getVideoById(request):
    videoId = request.GET.get('id')
    try:
        video = Recording.objects.get(pk=videoId)
    except Recording.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VideoSerializer(video)
    return Response(serializer.data)


# returns list of all videos
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def getAllVideos(request):
    listOfVideo = []
    videoSet = Recording.objects.all()
    for instance in videoSet:
        info = {}
        info["id"] = instance.pk
        info["rid"] = instance.rid_id
        info["time"] = instance.time
        info["date"] = instance.date
        info["roomName"] = Raspberry.objects.get(pk=instance.rid_id).name
        listOfVideo.append(info)

    return Response({"videos": listOfVideo}, status=200)


@api_view(['GET'])
def getVideosByRoom(request):
    listOfVideo = []
    roomId = request.GET.get('rid')
    videoSet = Recording.objects.filter(rid=roomId)
    for instance in videoSet:
        info = {}
        info["id"] = instance.pk
        info["rid"] = instance.rid_id
        info["time"] = instance.time
        info["date"] = instance.date
        info["roomName"] = Raspberry.objects.get(pk=instance.rid_id).name
        listOfVideo.append(info)

    return Response({"videos": listOfVideo}, status=200)


@api_view(['GET'])
@only_rasps
def testPiToken(request):
    return Response({"detail": "Decorator works"}, status=200)


@api_view(['GET'])
def videoProt(request):
    videoId = request.GET.get('id')
    try:
        video = Recording.objects.get(pk=videoId)
        path = video.file.name  # Get the file path from the FieldFile
        file = default_storage.open(path)  # Open the file using the default storage
        return FileResponse(file)
    except Recording.DoesNotExist:
        return Response("Video not found", status=status.HTTP_404_NOT_FOUND)


# returns system logs
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def getSysLogs(request):
    logSet = SystemAlertLog.objects.all()
    serializer = SystemAlertLogSerializer(logSet, many=True)
    return Response({"logs": serializer.data}, status=200)


def send_email_alarm(mail, room):
    em = EmailMessage()
    em['From'] = emailSender
    em['To'] = str(mail)
    em['Subject'] = subject = 'Emergency: Alarm in Room: ' + room
    full = f"{body}{room}"
    em.set_content(full)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(emailSender, emailPassword)
        smtp.sendmail(emailSender, mail, em.as_string())


def init_sending_emails(room):
    users = get_all_user_emails()
    for email in users:
        send_email_alarm(email, room)


def get_all_user_emails():
    users = User.objects.all()
    user_emails = []
    for user in users:
        user_emails.append(user.email)
    return user_emails
