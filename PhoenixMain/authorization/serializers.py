from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password':{'write_only':True}}




class VideoUploadSerializer(serializers.Serializer):
    video_file = serializers.FileField()