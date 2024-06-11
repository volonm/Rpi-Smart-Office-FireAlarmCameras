from django.urls import path, re_path

from . import tests
from . import views

urlpatterns = [
    re_path('sensorData', views.receiveSensorData),  # post for getting data from sensor module
    re_path('systemAlarm', views.alertStatus),  # post to start server alarm
    re_path('getSysStatus', views.getSysStatus),  # returns system status of a server as "alertStatus"
    re_path('createSensorEntry', views.createSensorEntry),  # api to create an entry and returns  token and id of rsp
    re_path('stopAlert', views.stopAlert),  # stops alert  in the system
    re_path('uploadVideo', views.uploadVideo),  # api to upload videos from sensor model to the server
    re_path('getVideoById', views.getVideoById),  # returns file path to  video by id
    re_path('media', views.videoProt),  # returns media
    re_path('testAu', views.testPiToken),  # api to test pi token
    re_path('getAllVideos', views.getAllVideos),  # returns a list of all videos
    re_path('getVideosByRoom', views.getVideosByRoom),  # returns a list of all videos
    re_path('getSysLogs', views.getSysLogs),  # returns system logs ( How triggered an alert and when it was stopped )
    re_path('injectRawData', tests.createRawData),
    re_path('deleteRawData', tests.delete_tested)
]
