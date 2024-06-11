import json
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views import View
from pywizlight.exceptions import WizLightTimeOutError
from lamp.models import Lamps
from pywizlight import discovery, wizlight, PilotBuilder
from asgiref.sync import sync_to_async
from authorization.decorators import session_valid
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# Request --> Response.


class LampControl(View):
    start = 0
    end = 0
    @staticmethod
    @sync_to_async
    def create_lamp(ip, mac, all_lamps):
        existing_lamp = all_lamps.filter(ipaddressV4=ip, macaddress=mac)
        if not existing_lamp:
            lamp = Lamps.objects.create(ipaddressV4=ip, macaddress=mac)
            lamp.save()

    @staticmethod
    @sync_to_async
    def delete_lamp(ip):
        print("lamp is going to be deleted")

        Lamps.objects.filter(ipaddressV4=ip).delete()

    @staticmethod
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @session_valid
    async def discover_add_lamps(request):
        print("Discover in PROGRESS")
        bulbs_dict = await discovery.discover_lights()
        print("Discover FINISHED")
        print(bulbs_dict)
        all_lamps = Lamps.objects.all()
        for bulb in bulbs_dict:
            await LampControl.create_lamp(bulb.ip, bulb.mac, all_lamps)
            print(bulb.__dict__)
        return HttpResponse(request)

    @staticmethod
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @session_valid
    async def turn_on(request):
        if request.method == 'POST':
            received_data = json.loads(request.body)
            try:
                ip_addr = received_data['ip']
                print(ip_addr)
                await wizlight(ip_addr).turn_on(PilotBuilder(brightness=255, cold_white=255))
            except KeyError:
                HttpResponseServerError("No ip address of a bulb received")
            return HttpResponse(request)

    @staticmethod
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @session_valid
    async def turn_off(request):
        if request.method == 'POST':
            received_data = json.loads(request.body)
            try:
                ip_addr = received_data['ip']
                await wizlight(ip_addr).turn_off()
            except KeyError:
                HttpResponseServerError("No ip address of a bulb received")
            return HttpResponse(request)

    @staticmethod
    def hex_to_rgb(value: object.__str__) -> tuple:
        rgb = []
        for i in (0, 2, 4):
            decimal = int(value[i:i + 2], 16)
            rgb.append(decimal)

        return tuple(rgb)

    @staticmethod
    def rgb_to_hex(tup: tuple) -> str:
        r = tup[0]
        g = tup[1]
        b = tup[2]
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    @staticmethod
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @session_valid
    async def set_color(request):
        if request.method == 'POST':
            received_data = json.loads(request.body)
            try:
                ip_addr = received_data['ip']
                color = LampControl.hex_to_rgb(received_data['c'])
                await wizlight(ip_addr).turn_on(PilotBuilder(rgb=color))
            except KeyError:
                HttpResponseServerError("No ip or color address of a bulb received")
            return HttpResponse(request)

    @staticmethod
    async def get_current_color(ipaddr):
        state = await wizlight(ipaddr).updateState()
        print(state.get_colortemp())
        return state.get_colortemp()

    @sync_to_async
    def get_all_ips(self):
        bulb_from_query = Lamps.objects.all()
        all_ip = []
        for bulb in bulb_from_query.iterator():
            # print(bulb.ipaddressV4)
            all_ip.append(bulb.ipaddressV4)
        return all_ip

    @staticmethod
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @session_valid
    async def lamps_page(request):
        start = time.time()
        all_ip = await LampControl.get_all_ips()  # Await the result of get_all_ips
        bulb_states = []
        for ip in all_ip:
            state = 0
            try:
                state = await wizlight(ip).updateState()
            except WizLightTimeOutError or RuntimeError:
                await LampControl.delete_lamp(ip)
            if state != 0:
                col = state.get_rgb()
                print(col)
                if col is None or col == (None, None, None):
                    col = (0, 0, 0)
                print(LampControl.rgb_to_hex(col))
                print(ip)
                bulb_states.append({'ipaddressV4': ip, 'color': LampControl.rgb_to_hex(col)})
        end = time.time()
        print(end - start)
        return render(request, 'lamps.html', {'bulbs_dict': bulb_states})
