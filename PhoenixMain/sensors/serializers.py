from rest_framework import serializers
from .models import SensorData, SystemAlertLog
from .models import Raspberry
from .models import Recording


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SensorData
        fields = ['TEMP', 'CO', 'H2', 'CH4', 'LPG', 'PROPANE', 'ALCOHOL', 'SMOKE', 'rid']


class SensorDataSerializerDateTime(serializers.ModelSerializer):
    class Meta(object):
        model = SensorData
        fields = ['date', 'time', 'TEMP', 'CO', 'H2', 'CH4', 'LPG', 'PROPANE', 'ALCOHOL', 'SMOKE']


class SensorDataSerializerDateTimeRid(serializers.ModelSerializer):
    class Meta(object):
        model = SensorData
        fields = ['date', 'time', 'TEMP', 'CO', 'H2', 'CH4', 'LPG', 'PROPANE', 'ALCOHOL', 'SMOKE', 'rid']


class SensorInitSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Raspberry
        fields = ['name']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'
        extra_kwargs = {'rid': {'write_only': True}}


class VideoUploadSerializer(serializers.Serializer):
    rid = serializers.IntegerField(required=False)
    video_file = serializers.FileField()


class SystemAlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAlertLog
        fields = '__all__'
