from django.urls import include, path
from inventario.views import bodegaRegistro, consultarcategorias

urlpatterns = [
    path('bodegaregistro', bodegaRegistro, name='registro'),
    path('consultarcategorias', consultarcategorias, name='consultarcategorias')
]
