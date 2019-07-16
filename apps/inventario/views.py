from django.shortcuts import render
#from inventario.aniadirCategoriaForm import AniadirCategoriaForm
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from inventario.models import Categoria, Proveedor

# Create your views here.

def categoria(request, *args, **kwargs):
    return render(request, "inventario/categoria.html", {})

@csrf_protect
def aniadirCategoria(request, *args, **kwargs):
    if request.method == 'POST':
        crear = request.POST
        nombre = crear.get('nombreCategoria')
        aux = Categoria( nombreCategoria = nombre )
        try:
            aux.full_clean()
        except ValidationError as e:
            return render(request, "inventario/categoria.html",{})
        aux.save()
    return render(request, "inventario/categoriaCrear.html", {})

def productos(request, *args, **kwargs):
    return render(request, "inventario/productos.html", {})

def aniadirProductos(request, *args, **kwargs):
    return render(request, "inventario/productosCrear.html", {})


def proveedor(request, *args, **kwargs):
    return render(request, "inventario/proveedor.html", {})

def aniadirProveedor(request, *args, **kwargs):
    if request.method == 'POST':
        crear = request.POST
        nit = crear.get('nitProveedor')
        direccion = crear.get('direccionProveedor')
        telefono = crear.get('telefonoProveedor')

        aux = Proveedor( pknit = nit, direccion = direccion, telefono = telefono)
        
        try:
            aux.full_clean()
        except ValidationError as e:
            
            return render(request, "inventario/proveedorCrear.html",{})
        aux.save()
    return render(request, "inventario/proveedorCrear.html", {})