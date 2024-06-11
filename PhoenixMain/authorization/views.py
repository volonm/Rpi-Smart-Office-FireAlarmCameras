import random
import secrets
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from email.message import EmailMessage
import smtplib
import string
import ssl
from .decorators import session_valid
from rest_framework.authtoken.models import Token
from datetime import datetime
from .models import SessionToken
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

TokenDictionary = {}


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def updateUser(request):
    auth_id = request.user.id
    uid = request.data['uid']
    old_password = request.data['password']
    new_pass = request.data['new_password']
    email = request.data['email']
    username = request.data['username']
    if uid:
        if int(auth_id) == int(uid):
            try:
                user = User.objects.get(id=uid)
                if not user.check_password(old_password):
                    return Response({"error": "The user old password is not correct"}, status=400)
                if new_pass:
                    user.set_password(new_pass)
                if email:
                    user.email = email
                if username:
                    user.username = username
                user.save()
                return Response({'detail': 'User changed successfully'})
            except User.DoesNotExist:
                return Response({"error": "The user id is not correct"}, status=400)

        return Response({'error': 'Invalid request method'}, status=405)
    return Response({'error': 'You can not update other Users'}, status=405)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_all_user_details(request):
    users = User.objects.all()
    if users:
        user_data = []

        for user in users:
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            user_data.append(user_info)
        return JsonResponse({'users': user_data})
    return JsonResponse({'error': 'This is not supposed to happen '}, status=405)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def updateUser(request):
    auth_id = request.user.id
    uid = request.data['uid']
    old_password = request.data['password']
    new_pass = request.data['new_password']
    email = request.data['email']
    username = request.data['username']
    if uid:
        if int(auth_id) == int(uid):
            try:
                user = User.objects.get(id=uid)
                if not user.check_password(old_password):
                    return Response({"error": "The user old password is not correct"}, status=400)
                if new_pass:
                    user.set_password(new_pass)
                if email:
                    user.email = email
                if username:
                    user.username = username
                user.save()
                return Response({'detail': 'User changed successfully'})
            except User.DoesNotExist:
                return Response({"error": "The user id is not correct"}, status=400)

        return Response({'error': 'Invalid request method'}, status=405)
    return Response({'error': 'You can not update other Users'}, status=405)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_all_user_details(request):
    users = User.objects.all()
    if users:
        user_data = []

        for user in users:
            user_info = {
                'uid': user.id,
                'username': user.username,
                'email': user.email,
            }
            user_data.append(user_info)
        return JsonResponse({'users': user_data})
    return JsonResponse({'error': 'This is not supposed to happen '}, status=405)
@api_view(['POST'])
def login(request):
    current_datetime = datetime.now()
    username = request.data['username']
    logSystemActivity(f"User {username} try to log in at {current_datetime:%Y-%m-%d %H:%M:%S} \n")
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"details": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    response = JsonResponse({"user": serializer.data, "token": token.key})
    response.set_cookie('account_token', token.key, httponly=True, secure=True)
    return response


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_email_code(request):
    token = request.headers['Authorization']
    pure_token = str(token).replace("Token ", "")
    email = request.user.email
    send_verification_code(email, pure_token)
    return Response({"2FA": "Email sent"})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tokenTest(request):
    return Response({"passed for {}".format(request.user.email)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def getUserByToken(request):
    return Response({"user": {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email
    }}, status=200)


def authorizationPage(request):
    return render(request, "authorization.html")


def logSystemActivity(information):
    try:
        with open('logs.txt', 'a') as file:
            file.write(information)
    except IOError as e:
        print("An error occurred while writing to logs")


emailSender = 'phoenix.firealarm@gmail.com'
emailPassword = 'lgej jkke dwsc ekfr'

subject = 'Somebody Is Trying to Login'
body = ("Welcome our Favourite Client"
        "\nThe verification code is ")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_account(request):
    code = request.data.get('code')
    token = request.headers['Authorization']
    if code and token:
        pure_token = str(token).replace("Token ", "")
        code_from_dict = str(TokenDictionary.get(pure_token))
        if str(code_from_dict) == str(code):
            session_token = secrets.token_hex(32)
            user = request.user
            print(id)
            session = create_session(user, session_token)
            return Response({"session": session}, status=200)
    return Response({"Given INCORRECT verification code:" + code + "  " + token}, status=status.HTTP_400_BAD_REQUEST)


def send_verification_code(email, token):
    if valid_email(email):
        em = EmailMessage()
        em['From'] = emailSender
        em['To'] = str(email)
        em['Subject'] = subject
        characters = string.ascii_letters + string.digits
        code = ''.join(random.sample(characters, 6))
        TokenDictionary[token] = code
        full = f"{body}{code}"
        em.set_content(full)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(emailSender, emailPassword)
            smtp.sendmail(emailSender, email, em.as_string())


def valid_email(email):
    user_exists = User.objects.filter(email=email).exists()
    if user_exists:
        return True
    else:
        return False


def create_session(user, session_token):
    token_query = Token.objects.filter(user_id=user.id)
    if token_query:
        session = SessionToken(userID=user, session=session_token)
        session.save()
        return session_token
    return None


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def only_with_2tokens(request):
    return Response({"EVERYTHING WORKS"})
