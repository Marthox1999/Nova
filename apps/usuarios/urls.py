from django.urls import include, path
from usuarios.views import ingreso, duenioIngreso


urlpatterns = [
    path('', ingreso, name='ingreso'),
    path('duenioIngreso/', duenioIngreso, name='duenioIngreso'),
]