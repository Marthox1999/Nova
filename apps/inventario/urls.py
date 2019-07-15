from django.urls import include, path
from inventario.views import bodegaRegistro, consultarcategorias, bodegaInicio

urlpatterns = [
    path('bodegainicio', bodegaInicio, name='bodegainicio'),
    path('bodegaregistro', bodegaRegistro, name='registro'),
    path('consultarcategorias', consultarcategorias, name='consultarcategorias')
]
