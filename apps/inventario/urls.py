from django.urls import include, path
from inventario.views import *

app_name='inventario'

urlpatterns = [
    path('modificarCategoria/',modificar_categoria,name='modificar_categoria'),
    path('categoria', categoria, name='categoria'),
    path('categoriaCrear', aniadirCategoria, name='aniadirCategoria'),
    path('categoriaModificar', modificar_categoria, name='modificar_categoria'),
    path('productos', productos, name='productos'),
    path('productosCrear', aniadirProductos, name='aniadirProductos'),
    path('proveedor', proveedor, name='proveedor'),
    path('proveedorCrear', aniadirProveedor, name='aniadirProveedor'),

]