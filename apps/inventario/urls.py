from django.urls import include, path

from inventario.views import modificar_categoria

urlpatterns = [
    #path('', ingreso, name='ingreso'),
    path('modificarCategoria/',modificar_categoria,name='modificar_categoria'),
]