import json
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sensors.models import SensorData, Raspberry
from sensors.serializers import SensorDataSerializerDateTime
from authorization.decorators import session_valid
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


@api_view(['GET'])
def testReact(response):
    return Response(status=200)


# returns list of all rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def getRooms(request):
    listOfRooms = []
    allRooms = Raspberry.objects.all()
    for room in allRooms:
        roomIdName = {}
        roomId = room.id
        roomName = room.name
        roomIdName['id'] = roomId
        roomIdName['name'] = roomName
        listOfRooms.append(roomIdName)

    return Response({"rooms": listOfRooms}, status=200)


# Returns json with the room with average temperature for last 24 hours.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_temp_average_rooms(request):
    current_time = timezone.now()
    time_24_ago = current_time - timedelta(hours=24)
    rasp_query = Raspberry.objects.all()
    list_temperature = []
    for pi in rasp_query:
        rpi_object = {}
        av_temp = 0
        sensor_query = SensorData.objects.filter(
            Q(date=time_24_ago.date(), time__gte=time_24_ago.time()) | Q(date__gt=time_24_ago.date()), rid=pi.id
        )
        if sensor_query:
            print(pi.name)
            for temp in sensor_query:
                print(temp.TEMP)
                av_temp += temp.TEMP
            av_temp = av_temp / sensor_query.count()
        rpi_object['id'] = pi.id
        rpi_object['name'] = pi.name
        rpi_object['average_temp'] = av_temp
        list_temperature.append(rpi_object)
    return Response({"rooms": list_temperature}, status=200)


# Returns json of all metrics within a room with a certain id for last 7 days
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_average_metric_room_week(request):
    received_id = request.GET.get('id')
    print(received_id)
    if received_id is not None and received_id.isnumeric():
        # List metrics includes dictionary elements which include all metrics including date
        list_metrics = []
        time_now = timezone.now()
        for i in range(0, 7):
            metrics_dict = {}
            av_temp = 0
            av_co = 0
            av_h2 = 0
            av_ch4 = 0
            av_lpg = 0
            av_propane = 0
            av_alcohol = 0
            av_smoke = 0
            delta = timezone.timedelta(days=i)
            days_ago = time_now - delta
            query_for_day = SensorData.objects.filter(date=days_ago.date(), rid=received_id)
            number_of_records = 1
            if query_for_day:
                number_of_records = query_for_day.count()
                for record in query_for_day:
                    av_temp += record.TEMP
                    av_co += record.CO
                    av_h2 += record.H2
                    av_ch4 += record.CH4
                    av_lpg += record.LPG
                    av_propane += record.PROPANE
                    av_alcohol += record.ALCOHOL
                    av_smoke += record.SMOKE
            serializer = SensorDataSerializerDateTime({
                'date': days_ago.date(),
                'time': "00:00",
                'TEMP': av_temp / number_of_records,
                'CO': av_co / number_of_records,
                'H2': av_h2 / number_of_records,
                'CH4': av_ch4 / number_of_records,
                'LPG': av_lpg / number_of_records,
                'PROPANE': av_propane / number_of_records,
                'ALCOHOL': av_alcohol / number_of_records,
                'SMOKE': av_smoke / number_of_records,
            })
            list_metrics.append(serializer.data)
        return Response({"average_per_7_days": list_metrics}, status=200)
    return Response({"id": "Id not given"}, status=status.HTTP_404_NOT_FOUND)


# Returns json of today's records
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_all_metric_room_today(request):
    received_id = request.GET.get('id')
    if received_id is not None and received_id.isnumeric():
        list_metrics = []
        date_today = timezone.now().date()
        query_for_day = SensorData.objects.filter(date=date_today, rid=received_id)
        if query_for_day:
            for record in query_for_day:
                serializer = SensorDataSerializerDateTime({
                    'date': record.date,
                    'time': record.time,
                    'TEMP': record.TEMP,
                    'CO': record.CO,
                    'H2': record.H2,
                    'CH4': record.CH4,
                    'LPG': record.LPG,
                    'PROPANE': record.PROPANE,
                    'ALCOHOL': record.ALCOHOL,
                    'SMOKE': record.SMOKE,
                })
                list_metrics.append(serializer.data)
            print(list_metrics)
            return Response(list_metrics, status=200)
        return Response([], status=200)
    return Response({"id": "Id not given"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def get_metrics_room_day(request):
    received_id = request.GET.get('id')
    start = request.GET.get('start')
    end = request.GET.get('end')
    all_data = []
    # If we receive id
    if received_id is not None and received_id.isnumeric():
        # If we receive dates
        if is_valid_timezone_date(start) and is_valid_timezone_date(end):
            start_timezone = timezone.make_aware(timezone.datetime.strptime(start, "%Y-%m-%d"))
            inclusive_date = timezone.make_aware(timezone.datetime.strptime(end, "%Y-%m-%d"))
            end_timezone = inclusive_date + timezone.timedelta(days=1)
            sensor_query = SensorData.objects.filter(
                Q(date__range=(start_timezone.date(), end_timezone.date()))
                & Q(rid=received_id))
            for record in sensor_query:
                serializer = SensorDataSerializerDateTime({
                    'date': record.date,
                    'time': record.time,
                    'TEMP': record.TEMP,
                    'CO': record.CO,
                    'H2': record.H2,
                    'CH4': record.CH4,
                    'LPG': record.LPG,
                    'PROPANE': record.PROPANE,
                    'ALCOHOL': record.ALCOHOL,
                    'SMOKE': record.SMOKE,
                })
                all_data.append(serializer.data)
            return Response({"selected_days": all_data}, status=200)
        return Response({"Time": "Time given incorrectly"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"id": "Id not given"}, status=status.HTTP_404_NOT_FOUND)


def is_valid_timezone_date(date_string):
    try:
        date_obj = timezone.make_aware(timezone.datetime.strptime(date_string, "%Y-%m-%d"))
        return True  # The date is valid and can be converted to a timezone-aware datetime.
    except ValueError:
        return False  # The date is not valid.


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@session_valid
def rename_room(request):
    data = json.loads(request.body)
    if data:
        print(data)
        received_name = data.get('name')
        received_id = data.get('id')
        print(received_name)
        if received_id and received_name:
            rasp_query = Raspberry.objects.get(id=received_id)
            if rasp_query:
                rasp_query.name = received_name
                rasp_query.save()
                return Response({"Room Changed"}, status=200)
    return Response({"detail": "Can not rename the room."}, status=400)
