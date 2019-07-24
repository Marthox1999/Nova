from django.urls import include, path

from ventas.views import *

app_name='ventas'
urlpatterns = [
    path('descuentos', descuentos, name='descuentos'),
    path('descuentoCrear', crearDescuento, name='descuentoCrear'),
    path('descuentoCrear/<int:idCategoria>', crearDescuentoCategoria, name='descuentoCrearCategoria'),
    path('descuentoCrear/<int:idCategoria>/<int:idSubCategoria>', crearDescuentoSubCategoria, name='descuentoCrearSubCategoria'),
    path('descuentoCrear/<int:idCategoria>/<int:idSubCategoria>/<int:idProducto>', crearDescuentoSubCategoria, name='descuentoCrearSubCategoria'),
]