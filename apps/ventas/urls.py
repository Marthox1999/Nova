from django.urls import include, path

from ventas.views import *

app_name='ventas'
urlpatterns = [
    path('descuentos', descuentos, name='descuentos'),
    path('aniadirDescuentos', aniadirDescuentos, name='aniadirDescuentos'),
]