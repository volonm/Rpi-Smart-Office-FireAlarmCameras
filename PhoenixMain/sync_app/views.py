import secrets
import string

from django.shortcuts import render
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.management import call_command

from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

import os

from authorization.decorators import only_rasps
from django.shortcuts import render

# Create your views here.

@api_view(['POST'])
def receiveCloudCredentials(request):
    if not request.data:
        return Response({'message': 'Invalid JSON data'}, status=400)

    try:
        server = request.data.get('server', '')
        database = request.data.get('database', '')
        user = request.data.get('user', '')
        password = request.data.get('password', '')
        driver = request.data.get('driver', '')
        connection_string = request.data.get('connection_string', '')
        container_name = request.data.get('container_name', '')

        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloudCredentials.txt')

        with open(config_file, 'w') as f:
            f.write(f"server={server}\n")
            f.write(f"database={database}\n")
            f.write(f"user={user}\n")
            f.write(f"password={password}\n")
            f.write(f"driver={driver}\n")
            f.write(f"connection_string={connection_string}\n")
            f.write(f"container_name={container_name}\n")

        return Response({'message': 'Data was received and processed'}, status=200)
    except Exception as e:
        return Response({'message': str(e)}, status=400)

