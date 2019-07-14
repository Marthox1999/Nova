from django.urls import include, path

from inventario.views import *

app_name='inventario'
urlpatterns = [
    
    path('aniadirCategoria', aniadirCategoria, name='aniadirCategoria'),
    path('categoria', categoria, name='categoria'),
]