from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum



from inventario.models import *
from ventas.models import *
# Create your views here.

def masVendidos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    
    productos = DetallesFactura.objects.values('fkDetallesP__fkProducto__fkSubCategoria__nombreSubCategoria', 'fkDetallesP__fkProducto__fkSubCategoria__fkCategoria__nombreCategoria', 'fkDetallesP__fkProducto__pkProducto', 'fkDetallesP__fkProducto__nombre').annotate(total=Sum('cantidad')).order_by('-total')[:20]
    
    context={'categorias':categorias, 'productos': productos, 'masOMenos': 'Más'}
    return render(request, 'reportes/vendidos.html', context, {})

    

def menosVendidos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    
    productos = DetallesFactura.objects.values('fkDetallesP__fkProducto__fkSubCategoria__nombreSubCategoria', 'fkDetallesP__fkProducto__fkSubCategoria__fkCategoria__nombreCategoria', 'fkDetallesP__fkProducto__pkProducto', 'fkDetallesP__fkProducto__nombre').annotate(total=Sum('cantidad')).order_by('total')[:20]
    
    context={'categorias':categorias, 'productos': productos, 'masOMenos': 'Menos'}
    return render(request, 'reportes/vendidos.html', context, {})