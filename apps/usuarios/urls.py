from django.urls import include, path
from django.contrib.auth import views as auth_views
from usuarios.views import clienteIngreso, clienteCerrarSesion, clienteInicio, clienteRegistro

app_name = 'usuarios'

urlpatterns = [
    path('clienteingresar', clienteIngreso, name='ingresoCliente'),
    path('clienteregistro',clienteRegistro, name='registroCliente'),
    path('clientecerrarsesion', clienteCerrarSesion, name='cerrarSesionCliente'),
    path('clienteinicio', clienteInicio, name='inicioCliente'),
]
