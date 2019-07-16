from django.urls import include, path
from usuarios.views import duenioAdminIngreso, paginaPrincipal_duenio, duenioAdminAgregar, paginaPrincipal_admin, ingreso, adminMenu

app_name='usuarios'

urlpatterns = [
    path('', ingreso, name='ingreso'),
    #path('principalAdmin/<int:id_dueno>/',paginaPrincipal_admin,name='paginaPrincipal_admin'),
    path('principalAdmin/',paginaPrincipal_admin,name='paginaPrincipal_admin'),
    path('duenioAdminIngreso/', duenioAdminIngreso, name='duenioAdminIngreso'),
    path('principalDuenio/', paginaPrincipal_duenio, name='paginaPrincipal_duenio'),
    #path('duenioAdminAgregar/', duenioAdminAgregar, name='duenioAdminAgregar'),
    #path('adminMenu/', adminMenu, name='adminMenu'),
    path('adminMenu/', adminMenu, name='duenioAdminMenu'),
    path('duenioAdminAgregar/', duenioAdminAgregar, name='duenioAgregarAdmin'),
]
