from django.urls import include, path

from usuarios.views import ingreso, registro

urlpatterns = [
    path('', ingreso, name='ingreso'),
    path('registroCliente',registro),
]