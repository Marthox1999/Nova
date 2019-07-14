from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from usuarios.models import Cliente

# Create your views here.
#from .forms import NameForm

def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})
  
@csrf_protect
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
        try:
            aux.full_clean()
        except ValidationError as e:
            messages.info(request, 'Algunos campos no son validos')
            return render(request, "usuarios/registroCliente.html",{})
        nombre =registrar.get('nombreCliente')
        aux.save()
        messages.success(request, f'{nombre} bienvenido(a) a Nova :D')
        return redirect(to='ingreso')

    return render(request, "usuarios/clienteregistro.html",{'form':registrar})

