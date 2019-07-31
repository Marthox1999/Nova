from django.urls import include, path
from inventario.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inventario'
urlpatterns = [
    path('bodegainicio', bodegaInicio, name='bodegainicio'),
    path('bodegaregistro', bodegaRegistro, name='bodegaregistro'),
    path('bodegaconsulta', bodegaconsulta, name='bodegaconsulta'),
    path('consultarcategorias', consultarcategorias, name='consultarcategorias'),
    path('modificarCategoria/',modificar_categoria,name='modificar_categoria'),
    path('categoria', categoria, name='categoria'),
    path('categoriaCrear', aniadirCategoria, name='aniadirCategoria'),
    path('categoriaModificar', modificar_categoria, name='modificar_categoria'),
    path('productos', productos, name='productos'),
    path('productosCrearPrincipal', productosCrearPrincipal, name='productosCrearPrincipal'),
    path('productosCrear', aniadirProductos, name='aniadirProductos'),
    path('referenciasCrear', aniadirReferencias, name='aniadirReferencias'),
    path('productosModificarPrincipal', productosModificarPrincipal, name='productosModificarPrincipal'),
    path('productosModificar', modificarProductos, name='modificarProductos'),
    path('referenciasModificar/<int:idCategoria>/<int:idSubCategoria>/<int:idProducto>', modificarReferencias, name='modificarReferencias'),
    path('proveedor', proveedor, name='proveedor'),
    path('proveedorCrear', aniadirProveedor, name='aniadirProveedor'),

]
