from django.urls import include, path

from inventario.views import *

app_name='inventario'
urlpatterns = [
    path('categoria', categoria, name='categoria'),
    path('categoriaCrear', aniadirCategoria, name='aniadirCategoria'),
    path('productos', productos, name='productos'),
    path('productosCrear', aniadirProductos, name='aniadirProductos'),
    path('proveedor', proveedor, name='proveedor'),
    path('proveedorCrear', aniadirProveedor, name='aniadirProveedor'),
]