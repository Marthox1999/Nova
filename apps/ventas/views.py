from django.shortcuts import render


# Create your views here.


def descuentos(request, *args, **kwargs):
    return render(request, "ventas/descuentos.html", {})

def aniadirDescuentos(request, *args, **kwargs):
    return render(request, "ventas/aniadirDescuentos.html", {})

