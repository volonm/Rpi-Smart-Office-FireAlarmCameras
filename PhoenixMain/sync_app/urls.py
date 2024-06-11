from django.urls import path, re_path
from . import views
from . import tests


urlpatterns = [
    re_path('cloudCredentials', views.receiveCloudCredentials),  # post for getting data from sensor module
]