from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils import timezone
from usuarios.models import Cliente
from inventario.models import Categoria

def clienteIngreso(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    ingresar = request.POST
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
            return redirect(to='inicioCliente')
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/clienteingreso.html', context,{'form':ingresar})

def clienteCerrarSesion(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, 'usuarios/clienteingreso.html', context, {})

def clienteInicio(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    print(categorias)
    return render(request, 'usuarios/clienteinicio.html', context, {})


@csrf_protect
def clienteRegistro(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
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
            return render(request, "usuarios/clienteregistro.html", context,{'form':registrar})
        nombre =registrar.get('nombreCliente')
        aux.save()
        messages.success(request, f'{nombre} bienvenido(a) a Nova :D')
        return redirect(to='ingreso')

    return render(request, "usuarios/clienteregistro.html", context,{'form':registrar})
