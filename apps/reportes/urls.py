from django.urls import include, path
from reportes.views import *

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'reportes'
urlpatterns = [
    path('inicioReportes', inicioReportes, name='inicioReportes'),
    path('reporteVentas', reporteVentas, name='reporteVentas'),
    path('reportePocasUnidades', reportePocasUnidades, name='reportePocasUnidades'),
    path('masVendidos/', masVendidos, name='masVendidos'),
    path('menosVendidos/', menosVendidos, name='menosVendidos'),
]
