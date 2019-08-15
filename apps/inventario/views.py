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
    print(modificar)
    idCategoria = modificar.get('categoria')#actualiza combobox
    idCategoriaSubCat = modificar.get('idCat')
    nombreSubCat = modificar.get('nombreSubCategoria')
    accionSubCatSubmit = modificar.get('SubCat-submit')
    acccionModCatSubmit = modificar.get('modfCat-submit')
    selectSubCat = modificar.get('subCategoria')#actualizar combobox subcategoria
    idSubCategoria = modificar.get('idSubCategoria')
    ###################################

    #modificar categoria
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
    ###########################
        
    #agregar subcategoria
    if(accionSubCatSubmit=="Agregar" and not(idCategoriaSubCat=='-1' or idCategoriaSubCat==None)):
        print("solicitudcorrecta")
        aux = SubCategoria(
            fkCategoria=Categoria.objects.get(pkCategoria=idCategoriaSubCat),
            nombreSubCategoria=nombreSubCat
        )        
        try:
            aux.full_clean()
        except ValidationError as e:
            context={'categorias':categorias}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/modificar_categoria.html", context, {})
        aux.save()
        context={'categorias':categorias}
        messages.success(request, 'SubCategoria agregada con exito')
        return render(request, "inventario/modificar_categoria.html", context, {})
    #########################

    #modificar subcategoria
    if(accionSubCatSubmit=="Modificar" and not(idSubCategoria==-1 or idSubCategoria==None)):
        try:
            idCat = SubCategoria.objects.filter(pkSubCategoria = idSubCategoria).first()
            aux = SubCategoria(
                fkCategoria= idCat.fkCategoria,
                nombreSubCategoria=nombreSubCat
            ) 
            aux.full_clean()
        except ValidationError as e:
            context={'categorias':categorias}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/modificar_categoria.html", context, {})
        SubCategoria.objects.filter(pkSubCategoria = idSubCategoria).update(nombreSubCategoria = aux.nombreSubCategoria)
        context={'categorias':categorias}
        messages.success(request, 'SubCategoria modificada con exito')
        return render(request, "inventario/modificar_categoria.html", context, {})        

    ##########################3

    #actualiza combobox categoria 
    subCategorias = {}
    subCat = ""
    nombreCategoria = ""
    nombreSubCategoria = ""
    if(idCategoria !='-1' and idCategoria != None):
        categoriaObject = Categoria.objects.get(pkCategoria=idCategoria)    
        nombreCategoria = categoriaObject.nombreCategoria
        subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)
    if (selectSubCat != '-1' and selectSubCat != None):
        subCat = SubCategoria.objects.filter(pkSubCategoria = selectSubCat)
        #print(subCat.nombreSubCategoria)
        nombreSubCategoria = subCat[0].nombreSubCategoria
    #actualiza combobox subcategoria

    context={'categorias':categorias, 'subCategorias':subCategorias, 'idCategoria':idCategoria, 'nombreCategoria':nombreCategoria, 'idSubCategoria': selectSubCat, 'nombreSubCategoria': nombreSubCategoria}
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
