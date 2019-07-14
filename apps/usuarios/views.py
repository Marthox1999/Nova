from django.shortcuts import render
from django.http import HttpResponse

from usuarios.models import Cliente

# Create your views here.
#from .forms import NameForm

def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})
  
def registro(request, *args, **kwargs):
    registrar = request.POST
    if(request.method == 'POST'):  
        aux = Cliente(
            nombre= registrar.get('nombreCliente'),
            clave = registrar.get('claveCliente'),
            fechaNacimiento = registrar.get('fechaNacimiento'),
            direccion = registrar.get('direccionCliente'),
            telefono = registrar.get('telefonoCliente'),
            tipoDocumento = registrar.get('tipoDocumento'),
            numeroDocumento = registrar.get('documentoCliente'),
        )
        aux.save()
        print('paso 0.0')
        return render(request, "usuarios/confirmacion.html",{})

    return render(request, "usuarios/registroCliente.html",{'form':registrar})

