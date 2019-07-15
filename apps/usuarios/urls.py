from django.urls import include, path
from usuarios.views import ingreso, duenioIngreso, paginaPrincipal_duenio, agregarAdmin


urlpatterns = [
    path('', ingreso, name='ingreso'),
    path('duenioIngreso/', duenioIngreso, name='duenioIngreso'),
    path('principalDuenio/', paginaPrincipal_duenio, name='paginaPrincipal_duenio'),
    path('agregarAdmin/', agregarAdmin, name='agregarAdmin'),
]