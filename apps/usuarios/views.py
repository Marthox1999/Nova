from django.shortcuts import render
from django.http import HttpResponse

from usuarios.models import crear
# Create your views here.
#from .forms import NameForm

def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})
  
def registro(request, *args, **kwargs):
    registrar = request.POST
    if(request.method == 'POST'):
        cliente = {
            'nombre': registrar.get('nombreCliente'),
            'direccion': registrar.get('direccionCliente'),
            'telefono': registrar.get('telefonoCliente'),
            'tipoDocumento': registrar.get('tipoDocumento'),
            'documento': registrar.get('documentoCliente'),
            'fechaNacimiento': registrar.get('fechaNacimiento')
        }
        respuesta = crear(cliente)
        return render(request, "usuarios/confirmacion.html",{})

    return render(request, "usuarios/registroCliente.html",{'form':registrar})

