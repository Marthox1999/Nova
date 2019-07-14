from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
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
            return redirect('/homepage')
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/ingreso.html',{'form':ingresar})

def clienteCerrarSesion(request, *args, **kwargs):
    return render(request, 'usuarios/ingreso.html',{})

def clienteInicio(request, *args, **kwargs):
    return render(request, 'usuarios/inicioCliente.html',{})
