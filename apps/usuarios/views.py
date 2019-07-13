from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.



def ingreso(request, *args, **kwargs):
    return render(request, "usuarios/ingreso.html", {})


def duenioIngreso(request, *args, **kwargs):
    return render(request, "usuarios/duenioIngreso.html", {})

def logout_request(request):
    logout(request)
    messages.info(request, "salio de la app")
    return redirect("usuarios:duenioIngreso.html")

def login_request(request):
    form = AuthenticationForm()
    return render(request, "usuarios/duenioIngreso.html", {"form":form})

