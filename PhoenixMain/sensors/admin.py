from django.contrib import admin
from sensors.models import Raspberry, SensorData, Recording, SystemStatus, SystemAlertLog

# Register your models here.
admin.site.register(Raspberry)
admin.site.register(SensorData)
admin.site.register(Recording)
admin.site.register(SystemStatus)
admin.site.register(SystemAlertLog)
