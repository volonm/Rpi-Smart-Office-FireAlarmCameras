from django.urls import path
from . import views

urlpatterns = [
    path('', views.LampControl.lamps_page),
    path('discovermode', views.LampControl.discover_add_lamps),
    path('on/', views.LampControl.turn_on),
    path('off/', views.LampControl.turn_off),
    path('color/', views.LampControl.set_color),
]

