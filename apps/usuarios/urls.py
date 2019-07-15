from django.urls import include, path
from usuarios.views import duenioAdminIngreso, paginaPrincipal_duenio, duenioAdminAgregar, adminMenu


urlpatterns = [
    path('duenioAdminIngreso/', duenioAdminIngreso, name='duenioAdminIngreso'),
    path('principalDuenio/', paginaPrincipal_duenio, name='paginaPrincipal_duenio'),
    path('duenioAdminAgregar/', duenioAdminAgregar, name='duenioAdminAgregar'),
    path('adminMenu/', adminMenu, name='adminMenu'),
    path('principalDuenio/adminMenu/', adminMenu, name='duenioAdminMenu'),
    path('principalDuenio/adminMenu/duenioAdminAgregar/', duenioAdminAgregar, name='duenioAgregarAdmin'),
]