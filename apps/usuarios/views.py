from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils import timezone
from usuarios.models import Cliente

def clienteIngreso(request, *args, **kwargs):
    ingresar = request.POST
    print(request)  
    if(request.method == 'POST'):
        aux = Cliente(
            nombre=ingresar.get('username'),
            clave=ingresar.get('password'),
            fechaNacimiento = timezone.now,
            direccion = "",
            telefono = "",
            tipoDocumento = "",
            numeroDocumento = 1234567,
        )
        nombre=ingresar.get('username')
        if (aux.autenticarCliente()):
            messages.success(request, f'¡Bienvenido {nombre}!')
            return redirect(to='usuarios:inicioCliente')
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/ingreso.html',{'form':ingresar})

def clienteCerrarSesion(request, *args, **kwargs):
    return render(request, 'usuarios/ingreso.html',{})

def clienteInicio(request, *args, **kwargs):
    return render(request, 'usuarios/inicioCliente.html',{})

   
@csrf_protect
def clienteregistro(request, *args, **kwargs):
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
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "usuarios/clienteregistro.html",{'form':registrar})
        nombre =registrar.get('nombreCliente')
        aux.save()
        messages.success(request, f'¡{nombre} bienvenido(a) a Nova!')
        return redirect(to='usuarios:ingreso')

    return render(request, "usuarios/clienteregistro.html",{'form':registrar})

def inicioAdministrador(request, *args, **kwargs):
    return render(request, "usuarios/inicioAdministrador.html", {})

