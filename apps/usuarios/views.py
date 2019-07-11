from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from usuarios.models import AdministradorDuenio


def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})

def paginaPrincipal_admin(request, *args, **kwargs):
    admin = AdministradorDuenio.objects.get(pkAdministradorDuenio=1)
    context = {
        'objeto' : admin
    }
    return render(request, "usuarios/paginaPrincipal_admin.html",context)