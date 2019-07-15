from django.urls import include, path
from inventario.views import bodegaRegistro

urlpatterns = [
    path('bodegaregistro', bodegaRegistro, name='registro'),
]
