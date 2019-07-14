from django.urls import include, path

from inventario.views import *

app_name='inventario'
urlpatterns = [
    path('categoria', categoria, name='categoria'),
    path('aniadirCategoria', aniadirCategoria, name='aniadirCategoria'),
    path('productos', productos, name='productos'),
    path('aniadirProductos', aniadirProductos, name='aniadirProductos'),
]