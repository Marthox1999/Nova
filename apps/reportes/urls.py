from django.urls import include, path
from reportes.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reportes'
urlpatterns = [
    path('inicioReportes', inicioReportes, name='inicioReportes'),
    path('reporteVentas', reporteVentas, name='reporteVentas'),
    path('reporteVentasCategoria', reporteVentasCategoria, name='reporteVentasCategoria'),
    path('reporteTopClientes', reporteTopClientes, name='reporteTopClientes'),
    path('reportePocasUnidades', reportePocasUnidades, name='reportePocasUnidades'),
]