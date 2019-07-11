from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def inicio(request, *args, **kwargs):
    return render(request, "ingreso.html", {})
 