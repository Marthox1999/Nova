from django.shortcuts import render
#from inventario.aniadirCategoriaForm import AniadirCategoriaForm
from django.http import HttpResponseRedirect


# Create your views here.

"""
def aniadirCategoria(request):
    if request.method == 'POST':
        form = AniadirCatgoriaForm(request.POST)
        if form.is_Valid():
            form.save()
        return HttpResponseRedirect('aniadirCategoria')
    else:
        form = AniadirCategoriaForm()

    return render(request, 'inventario/aniadirCategoriaForm.html', {'form':form})
"""

def categoria(request, *args, **kwargs):
    return render(request, "inventario/categoria.html", {})

def aniadirCategoria(request, *args, **kwargs):
    return render(request, "inventario/aniadirCategoria.html", {})

def productos(request, *args, **kwargs):
    return render(request, "inventario/productos.html", {})

def aniadirProductos(request, *args, **kwargs):
    return render(request, "inventario/aniadirProductos.html", {})