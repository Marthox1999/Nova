from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from inventario.models import *
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

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

def productosCrearPrincipal(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/productosCrearPrincipal.html",context, {})

def aniadirReferencias(request, *args, **kwargs):
    categorias = Categoria.objects.all()

    modificar = request.POST  
    print("#################")
    print(request.FILES)
    print("#################")
    idCategoria = modificar.get('categoria')
    submitReq = modificar.get('productos-submit')

    subCategorias = {}
    if(idCategoria=='-1' or idCategoria==None):
        subCategorias = {}
    else:
        categoriaObject = Categoria.objects.get(pkCategoria=idCategoria)    
        subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)

    #CREAR REFERENCIAS ------------------------------------
    idSubCat = modificar.get('subCategoria')
    nombre = modificar.get('inputNombre')
    descripcion = modificar.get('DescrProducto')
    if(modificar.get('inputPrecio')=="" or modificar.get('inputPrecio')==None):
        precio = 0
    else:
        precio = int(modificar.get('inputPrecio'))
    if(modificar.get('inputIva')=="" or modificar.get('inputIva')==None):
        iva = 0
    else:
        iva = int(modificar.get('inputIva'))*precio/100
    #imagen = request.FILES['buscadorImagen']
    #imagen = request.FILES['buscadorImagen']
    imagen = " "
    if(submitReq=="Crear Producto" and not(idSubCat=="null") and not(nombre=="") and not(descripcion=="") and not(iva<=0) and not(precio<=0) and not(imagen=="")):
        print(imagen)
        aux = Producto(
            fkSubCategoria = SubCategoria.objects.get(pkSubCategoria=idSubCat),
            nombre = nombre,
            descripcion = descripcion,
            iva = iva,
            precio = precio,
            rutaImagen = imagen
        )
        try:
            aux.full_clean()
        except ValidationError as e:
            context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/referenciasCrear.html", context, {})
        #aux.rutaImagen.save()
        aux.save()
        context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
        messages.success(request, 'Producto creado con exito')
        return render(request, "inventario/referenciasCrear.html", context, {})
    elif(submitReq=="Crear Producto"):
        context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
        messages.info(request, 'Alguno(s) campo(s) no son validos')
        return render(request, "inventario/referenciasCrear.html", context, {})

    context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
    return render(request, "inventario/referenciasCrear.html", context, {})

def aniadirProductos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    bodegas = Bodega.objects.all()

    modificar = request.POST  
    idCategoria = modificar.get('categoria')
    submitReq = modificar.get('productos-submit')

    subCategorias = {}
    if(idCategoria=='-1' or idCategoria==None):
        subCategorias = {}
    else:
        categoriaObject = Categoria.objects.get(pkCategoria=idCategoria)    
        subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)

    #AGREGAR PRODUCTOS ----------------------------------------------
    idProducto = modificar.get('producto')
    idProveedor = modificar.get('proveedor')
    idBodega = modificar.get('bodega')
    talla = modificar.get('talla')
    if(modificar.get('inputCant')=="" or modificar.get('inputCant')==None):
        cantidad = 0
    else:
        cantidad = int(modificar.get('inputCant'))
    color = modificar.get('inputColor')

    if(submitReq=="Agregar Productos" and not(idProducto=="-1") and not(idProveedor=="-1") and not(idBodega=="-1") and not(talla=="") and not(color=="") and not(cantidad<=0)):
        aux = DetallesProducto(
            fkProducto = Producto.objects.get(pkProducto=idProducto),
            talla = talla,
            nit = Proveedor.objects.get(pknit=idProveedor),
            color = color,
            fkBodega = Bodega.objects.get(pkBodega=idBodega),
            cantidad = cantidad,
        )        
        try:
            aux.full_clean()
        except ValidationError as e:
            context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/productosCrear.html", context, {})

        aux.save()
        context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
        messages.success(request, 'Productos agregados con exito')
        return render(request, "inventario/productosCrear.html", context, {})
    elif(submitReq=="Agregar Productos"):
        context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
        messages.info(request, 'Alguno(s) campo(s) no son validos')
        return render(request, "inventario/productosCrear.html", context, {})

    context={'categorias':categorias, 'idCategoria':idCategoria, 'subCategorias':subCategorias, 'productos':productos, 'proveedores':proveedores, 'bodegas':bodegas}
    return render(request, "inventario/productosCrear.html", context, {})

def productosModificarPrincipal(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/productosModificarPrincipal.html",context, {})

def modificarReferencias(request, idCategoria, idSubCategoria, idProducto):
    categorias = Categoria.objects.all()
    subcategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)
    productos = Producto.objects.filter(fkSubCategoria=idSubCategoria)
    categoria = idCategoria
    subcategoria = idSubCategoria
    producto = idProducto
    context={
        'categorias':categorias,
        'subcategorias':subcategorias, 
        'productos':productos,
        'categoria':categoria,
        'subcategoria':subcategoria,
        'producto':producto
        }
    print(context)

    if request.method == 'POST':
        data = request.POST

    return render(request, "inventario/referenciasModificar.html",context, {})

def modificarProductos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, "inventario/productosModificar.html",context, {})

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
