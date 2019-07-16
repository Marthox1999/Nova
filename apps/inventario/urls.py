from django.urls import include, path
from inventario.views import bodegaRegistro, consultarcategorias, bodegaInicio

app_name = 'inventario'
urlpatterns = [
    path('bodegainicio', bodegaInicio, name='bodegainicio'),
    path('bodegaregistro', bodegaRegistro, name='bodegaregistro'),
    path('consultarcategorias', consultarcategorias, name='consultarcategorias')
]
