from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def modificar_categoria(request, *args, **kwargs):
    return render(request, "inventario/modificar_categoria.html", {})