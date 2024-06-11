import random
from django.test import TestCase
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Raspberry, SensorData
from .serializers import SensorDataSerializerDateTimeRid

# Create your tests here.


room_names = ["Living Room Raw", "Bedroom Raw", "Kitchen Raw"]


@api_view(['POST'])
def delete_tested(request):
    for i in range(0, 3):
        rasp = Raspberry.objects.filter(name=room_names[i])
        rasp.delete()
    return Response({"detail": "Deleted Records"}, status=200)


@api_view(['POST'])
def createRawData(request):
    # creating three different Raspberry Pi entries if not exist
    for i in range(0, 3):
        try:
            ras = Raspberry.objects.get(name=room_names[i])
            if ras:
                print("The Raspberry Entry ")
        except Raspberry.DoesNotExist:
            raspberry = Raspberry(name=room_names[i])
            raspberry.save()

    for i in range(0, 3):
        rasp = Raspberry.objects.get(name=room_names[i])
        try:
            id = rasp.id
            print(id)
            delta = timezone.timedelta(hours=i + 2)
            for days in range(0, 5):
                server_time = timezone.now() - delta
                delta_days = timezone.timedelta(days=days)
                server_time -= delta_days

                for records in range(0, 11):
                    # Records will be added for each 5 time from
                    delta_minutes = timezone.timedelta(minutes=records * 5)
                    server_time += delta_minutes

                    # Random Temperatures, but higher with each id > previous ip
                    lowest_temp = 10 + i * 3
                    highest_temp = 30 - i * 3
                    temp = round(random.uniform(lowest_temp, highest_temp), 2)

                    # Random CO, but higher with each id > previous ip
                    highest_co = 3 + i * 3
                    co = round(random.uniform(0, highest_co), 2)

                    # Random H2, but between 20-30 for first two and 50-60 for last raspberry
                    if i < 1:
                        h2 = round(random.uniform(20, 30), 2)
                    else:
                        h2 = round(random.uniform(50, 60), 2)

                    # Random CH4,  but higher with each id > previous ip
                    lowest_ch4 = 0 + i * 3
                    highest_ch4 = 50 - i * 3
                    ch4 = round(random.uniform(lowest_ch4, highest_ch4), 2)

                    # Random LPG,  but higher with each id > previous ip
                    lpg = round(random.uniform(lowest_ch4, highest_ch4), 2)

                    # Random PROPANE,  but higher with each id > previous ip
                    propane = round(random.uniform(lowest_ch4, highest_ch4), 2)

                    # Random ALCOHOL,  but higher with each id > previous ip
                    alcohol = round(random.uniform(lowest_ch4, highest_ch4), 2)

                    # Random SMOKE,  but higher with each id > previous ip
                    smoke = round(random.uniform(lowest_ch4, highest_ch4), 2)

                    data_to_serialize = {'date': server_time.date(),
                                         'time': server_time.time(),
                                         'TEMP': temp,
                                         'CO': co,
                                         'H2': h2,
                                         'CH4': ch4,
                                         'LPG': lpg,
                                         'PROPANE': propane,
                                         'ALCOHOL': alcohol,
                                         'SMOKE': smoke,
                                         'rid': id}
                    serializer = SensorDataSerializerDateTimeRid(data=data_to_serialize)

                    if serializer.is_valid():
                        serializer.save()

        except Raspberry.DoesNotExist:
            print("Raspberry Entries Not Found!!!")
            return Response({'detail': "Raspberry Entries Not Found!!!"}, status=400)

    return Response({"detail""Data Added"}, status=200)
