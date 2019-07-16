from django.urls import include, path
from django.contrib.auth import views as auth_views
from usuarios.views import clienteIngreso, clienteCerrarSesion, clienteInicio, clienteregistro

app_name = 'usuarios'

urlpatterns = [
    path('clienteingresar', clienteIngreso, name='ingreso'),
    path('clienteregistro',clienteregistro, name='registro'),
    path('clientecerrarsesion', clienteCerrarSesion, name='cerrarsesion'),
    path('clienteinicio', clienteInicio, name='inicioCliente'),
  
]
 
