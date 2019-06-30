from django.shortcuts import render
from .models import Product
# Create your views here.
from django.http import HttpResponse


def inicio(request, *args, **kwargs):
    Product.objects.create(nombre='camisa',precio='2000')
    data = Product.objects.get(id =1)
    context = {
        'objeto': data
    }
    return render(request, "Inicio.html", context)

def administrador(request, *args, **kwargs):
    return render(request, "administrador.html", {})
