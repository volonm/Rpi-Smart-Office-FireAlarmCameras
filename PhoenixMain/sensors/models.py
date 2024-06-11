from django.db import models
from django.utils import timezone



# Create your models here.

class Raspberry(models.Model):
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=100)


class SensorData(models.Model):
    rid = models.ForeignKey(Raspberry, on_delete=models.CASCADE) #rid_id
    TEMP = models.FloatField()
    CO = models.FloatField()
    H2 = models.FloatField()
    CH4 = models.FloatField()
    LPG = models.FloatField()
    PROPANE = models.FloatField()
    ALCOHOL = models.FloatField()
    SMOKE = models.FloatField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)



class Recording(models.Model):
    rid = models.ForeignKey(Raspberry, on_delete=models.CASCADE) #rid_id
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    file = models.FileField(upload_to='documents/')


class SystemStatus(models.Model):
    status = models.BooleanField(default=False)


class SystemAlertLog(models.Model):
    rid = models.IntegerField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    msg = models.CharField(max_length=50)
