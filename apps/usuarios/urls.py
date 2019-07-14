from django.urls import include, path

from usuarios.views import ingreso, registro

urlpatterns = [
    path('clienteingresar', ingreso, name='ingreso'),
    path('clienteregistro',registro, name='registro'),
]