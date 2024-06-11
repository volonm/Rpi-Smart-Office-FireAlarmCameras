from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('testReact', views.testReact),
    re_path('getRooms', views.getRooms),

    # Returns json with the room with average temperature for last 24 hours.
    # Format: {"rooms":[{"id":1,"name":"Kitchen","average_temp":12.2222}, {}, ...]}
    re_path('getAverageAll', views.get_temp_average_rooms),

    # Returns json of all metrics within a room with a certain id within last 7 days
    # Format: {"average_per_7_days": [{"date": "2023-10-31","av_temp": 7.0, ...},{},{}]}
    re_path(r'getAverageRid', views.get_average_metric_room_week, name='get_average_rid'),

    # Returns json of all metrics within a room with a certain id within this day
    # Format: {"today": [{"time": "12:00","temp": 5.0, ...},{},{}]}
    re_path(r'getRoomMetricDay', views.get_all_metric_room_today, name='get_room_metric_date'),

    # Returns json of all metrics within a room with a certain id within this day
    # Link of Format: https://.../getRoomMetricPeriod?id=2&start=2023-10-31&end=2023-10-23
    # Format: {"selected_days":[{"date": "2023-10-27","time": "09:15:24.977727","TEMP": 25.5,CO": 0.5,...},{}]
    re_path(r'getRoomMetricPeriod', views.get_metrics_room_day, name='get_room_metric_period'),

    # Front sends {"name":"NEW NEEDED NAME", "rid":"1"} ---> Rename the room for "Undefined" Rooms after Initialization
    re_path('renameRoom', views.rename_room)

]
