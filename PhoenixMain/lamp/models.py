from django.db import models
from django.utils import timezone


# Create your models here.

class Lamps(models.Model):
    ipaddressV4 = models.CharField(max_length=15, primary_key=True)
    macaddress = models.CharField(max_length=12)
    state = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
