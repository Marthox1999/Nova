from django.urls import include, path

from usuarios.views import *

app_name='usuarios'
urlpatterns = [
    path('', ingreso, name='ingreso'),
    
    path('inicioAdministrador', inicioAdministrador, name='inicioAdministrador'),
]