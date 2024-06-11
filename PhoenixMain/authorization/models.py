from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class SessionToken(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
