from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lamps/', include('lamp.urls')),
    path('auth/', include('authorization.urls')),
    path('sensors/', include('sensors.urls')),
    path('api/', include('reactApi.urls')),
    path('cloud/', include('sync_app.urls')),
]
