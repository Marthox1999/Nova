from django.urls import include, path
from reportes.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reportes'
urlpatterns = [
    path('reporteVentas', reporteVentas, name='reporteVentas'),
]