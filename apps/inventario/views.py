from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from inventario.models import Bodega, Categoria, Proveedor

def bodegaInicio(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request,'inventario/bodegainicio.html', context,{})

@csrf_protect
def bodegaRegistro(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    crearBodega = request.POST
    if(request.method == 'POST'):
        bodega = Bodega(
            direccion = crearBodega.get('direccion'),
            ciudad = crearBodega.get('ciudad')
        )
        print(crearBodega.get('direccion'))
        print(crearBodega.get('ciudad'))
        try:
            bodega.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no es(son) validos')
            return render(request,'inventario/bodegaregistro.html', context,{'form':crearBodega})
        bodega.save()
        messages.success(request, 'La bodega ha sido creada correctamente')
        return redirect(to='inventario:registro')
        categorias = Categoria.objects.all()
        context={'categorias':categorias}
    return render(request, 'inventario/bodegaregistro.html', context,{'form':crearBodega})

def consultarcategorias(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request,'inventario/categoriasconsultar.html', context,{})

def categoria(request, *args, **kwargs):
    return render(request, "inventario/categoria.html", {})

def modificar_categoria(request, *args, **kwargs):
    return render(request, "inventario/modificar_categoria.html", {})
  
  
@csrf_protect
def aniadirCategoria(request, *args, **kwargs):
    if request.method == 'POST':
        crear = request.POST
        nombre = crear.get('nombreCategoria')
        aux = Categoria( nombreCategoria = nombre )
        try:
            aux.full_clean()
        except ValidationError as e:
            return render(request, "inventario/categoriaCrear.html",{})
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
