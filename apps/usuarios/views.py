from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})

def inicioAdministrador(request, *args, **kwargs):
    return render(request, "usuarios/inicioAdministrador.html", {})

