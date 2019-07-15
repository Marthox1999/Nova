from django.shortcuts import render, redirect
from django.http import HttpResponse
#from .models import 
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from usuarios.models import AdministradorDuenio
from django.contrib.auth.decorators import login_required
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

def paginaPrincipal_duenio(request, *args, **kwargs):
    duenio = AdministradorDuenio.objects.get(pkAdministradorDuenio=1)
    context = {
        'objeto' : duenio
    }
    return render(request, "usuarios/paginaPrincipal_duenio.html",context)


def duenioAdminAgregar(request, *args, **kwargs):
    agregar = request.POST
    if(request.method=='POST'):
        admin=AdministradorDuenio(
            nombreUsuario=agregar.get('nombreAdmin'), 
            clave=agregar.get('claveAdmin'),
            tipo='ADMIN'
        )
        try:
            admin.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "usuarios/duenioAdminAgregar.html",{'form':agregar})
        nombre =agregar.get('nombreAdmin')
        admin.save()
        messages.success(request, f'¡Bienvenido {nombre} !')
        return redirect(to='duenioAdminAgregar')
    return render(request,"usuarios/duenioAdminAgregar.html",{'form':agregar})
    

def adminMenu(request, *args, **kwargs):
    return render(request,"usuarios/adminMenu.html", {})


def duenioAdminIngreso(request, *args, **kwargs):
    ingresar = request.POST
    print(request)
    if(request.method == 'POST'):
        admin = AdministradorDuenio(
            nombreUsuario=ingresar.get('nombreDuenioAdmin'),
            clave=ingresar.get('claveDuenioAdmin'),
            tipo='ADMIN'
        )
        nombre=ingresar.get('nombreDuenioAdmin')
        if (admin.autenticarDuenioAdmin()):
            messages.success(request, f'¡Bienvenido {nombre}!')
            return redirect(to='paginaPrincipal_duenio')
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/duenioAdminIngreso.html',{'form':ingresar})

 

