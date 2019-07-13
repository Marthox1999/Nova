from django.shortcuts import render, redirect
from django.http import HttpResponse
#from .models import 
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from usuarios.models import AdministradorDuenio
from django.contrib.auth.decorators import login_required
# Create your views here.



def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})


def duenioIngreso(request, *args, **kwargs):
    return render(request, "usuarios/duenioIngreso.html", {})


def paginaPrincipal_duenio(request, *args, **kwargs):
    duenio = AdministradorDuenio.objects.get(pkAdministradorDuenio=1)
    context = {
        'objeto' : duenio
    }
    return render(request, "usuarios/paginaPrincipal_duenio.html",context)


def logout_request(request):
    logout(request)
    messages.info(request, "salio de la app")
    return redirect("usuarios:duenioIngreso.html")

def login_request(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"tu nombre de usuario es {username}")
                return redirect("usuarios/paginaPrincial_duenio.html")
            else:
                messages.error(request, "contrasenia o usuario incorrectos")
        else:
            messages.error(request, "contrasenia o usuario incorrectos")

    form = AuthenticationForm()
    return render(request, "usuarios/paginaPrincipal_duenio.html", {"form":form})

