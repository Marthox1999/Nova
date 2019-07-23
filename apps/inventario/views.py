from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from inventario.models import *
from django.core.exceptions import ValidationError
from django.contrib import messages


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
        return redirect(to='inventario:bodegaregistro')
        categorias = Categoria.objects.all()
        context={'categorias':categorias}
    return render(request, 'inventario/bodegaregistro.html', context,{'form':crearBodega})

def bodegaconsulta(request, *args, **kwargs):
    categorias = Categoria.objects.all() #para cargar las categorias en el navbar
    bodegas = Bodega.objects.all()

    modificar = request.POST
    idBodega = modificar.get('bodega')

    if(idBodega=='-1' or idBodega==None):
        ciudadBodega = ""
        dirBodega = ""
    else:
        BodegaObject = Bodega.objects.get(pkBodega=idBodega)
        ciudadBodega = BodegaObject.ciudad
        dirBodega = BodegaObject.direccion


    context={'categorias':categorias, 'bodegas':bodegas, 'ciudadBodega':ciudadBodega, 'dirBodega':dirBodega}    
    return render(request, 'inventario/bodegaconsulta.html', context, {})

def consultarcategorias(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request,'inventario/categoriasconsultar.html', context,{})

def categoria(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/categoria.html",context, {})

def modificar_categoria(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    modificar = request.POST  
    idCategoria = modificar.get('categoria')

    idCategoriaSubCat = modificar.get('idCat')
    nombreSubCat = modificar.get('nombreSubCategoria')
    accionSubCatSubmit = modificar.get('SubCat-submit')
    acccionModCatSubmit = modificar.get('modfCat-submit')

    if ( acccionModCatSubmit == "Modificar"):
        nombreCategoria = modificar.get('nombreCategoria')
        aux =  Categoria(nombreCategoria = nombreCategoria)
        try:
            aux.full_clean()
        except ValidationError as e:
            context={'categorias':categorias}
            messages.info(request, 'Nuevo nombre de categoria invalido')
            return render(request, "inventario/modificar_categoria.html", context, {})

        Categoria.objects.filter(pkCategoria = idCategoriaSubCat).update(nombreCategoria = aux.nombreCategoria)
        context={'categorias':categorias}
        messages.success(request, 'Categoria modificada exitosamente')
        return render(request, "inventario/modificar_categoria.html", context, {})

        

    if(accionSubCatSubmit=="Agregar" and not(idCategoriaSubCat=='-1' or idCategoriaSubCat==None)):
        aux = SubCategoria(
            fkCategoria=Categoria.objects.get(pkCategoria=idCategoriaSubCat),
            nombreSubCategoria=nombreSubCat
        )        
        try:
            aux.full_clean()
        except ValidationError as e:
            print("socorro")
            context={'categorias':categorias}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/modificar_categoria.html", context, {})

        aux.save()
        context={'categorias':categorias}
        messages.success(request, 'SubCategoria agregada con exito')
        return render(request, "inventario/modificar_categoria.html", context, {})

    subCategorias = {}
    if(idCategoria=='-1' or idCategoria==None):
        nombreCategoria = ""
        idCategoria = ""
        subCategorias = {}
    else:
        categoriaObject = Categoria.objects.get(pkCategoria=idCategoria)    
        nombreCategoria = categoriaObject.nombreCategoria
        subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)

    context={'categorias':categorias, 'subCategorias':subCategorias, 'idCategoria':idCategoria, 'nombreCategoria':nombreCategoria}
    return render(request, "inventario/modificar_categoria.html", context, {}) 

@csrf_protect
def aniadirCategoria(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    if request.method == 'POST':
        crear = request.POST
        nombre = crear.get('nombreCategoria')
        aux = Categoria( nombreCategoria = nombre )
        try:
            aux.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            context={'categorias':categorias}
            messages.success(request, 'SubCategoria agregada con exito')
            return render(request, "inventario/categoriaCrear.html",context, {})

        aux.save()
        messages.success(request, 'Categoria agregada con exito')
        
    return render(request, "inventario/categoriaCrear.html",context, {})

def productos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/productos.html",context, {})

def aniadirProductos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/productosCrear.html", context, {})


def proveedor(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/proveedor.html",context, {})

def aniadirProveedor(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    if request.method == 'POST':
        crear = request.POST
        nit = crear.get('nitProveedor')
        direccion = crear.get('direccionProveedor')
        telefono = crear.get('telefonoProveedor')
        aux = Proveedor( pknit = nit, direccion = direccion, telefono = telefono)
        try:
            aux.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            context={'categorias':categorias}
            return render(request, "inventario/proveedorCrear.html",context,{})
        aux.save()
    messages.success(request, 'Proveedor agregado con exito')
    return render(request, "inventario/proveedorCrear.html",context ,{})
