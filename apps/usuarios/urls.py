from django.urls import include, path
from django.contrib.auth import views as auth_views
from usuarios.views import clienteIngreso, clienteCerrarSesion, clienteInicio

urlpatterns = [
    path('clienteingresar', clienteIngreso, name='ingreso'),
    path('clientecerrarsesion', clienteCerrarSesion, name='cerrarsesion'),
    path('homepage', clienteInicio, name='inicioCliente'),
]
