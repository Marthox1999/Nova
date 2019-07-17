from django.urls import include, path
from usuarios.views import *
from django.contrib.auth import views as auth_views

app_name='usuarios'

urlpatterns = [
    #path('principalAdmin/<int:id_dueno>/',paginaPrincipal_admin,name='paginaPrincipal_admin'),
    path('principalAdmin',paginaPrincipal_admin,name='paginaPrincipal_admin'),
    path('duenioAdminIngreso/', duenioAdminIngreso, name='duenioAdminIngreso'),
    path('principalDuenio/', paginaPrincipal_duenio, name='paginaPrincipal_duenio'),
    path('adminMenu/', adminMenu, name='duenioAdminMenu'),
    path('duenioAdminAgregar/', duenioAdminAgregar, name='duenioAgregarAdmin'),
    path('clienteingresar', clienteIngreso, name='ingreso'),
    path('clienteregistro',clienteregistro, name='registro'),
    path('clientecerrarsesion', clienteCerrarSesion, name='cerrarsesion'),
    path('clienteinicio', clienteInicio, name='inicioCliente'),
]
