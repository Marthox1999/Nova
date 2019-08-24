from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum



from inventario.models import *
# Create your views here.

def masVendidos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    ingresar = request.POST
    
    
    productos = DetallesProducto.objects.annotate(total=Sum('cantidad')).order_by('-cantidad')[:20]
    
    context={'categorias':categorias, 'productos': productos}
    return render(request, 'reportes/masVendidos.html', context, {})