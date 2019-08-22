from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from inventario.models import *
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import math
from django.core.files import File
import os 


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

def eliminarCategorias(request, idCategoria):
    if(idCategoria != 0):
        try:
            Categoria.objects.get(pkCategoria=idCategoria).delete()
            categorias = Categoria.objects.all()
            context={'categorias':categorias}
            messages.success(request, 'Categoria eliminada exitosamente')
            return render(request,'inventario/categoriasEliminar.html', context,{})
        except:
            categorias = Categoria.objects.all()
            context={'categorias':categorias}
            messages.warning(request, 'Esta categoria ya ha sido eliminada')
            return render(request,'inventario/categoriasEliminar.html', context,{})
    else:
        categorias = Categoria.objects.all()
        context={'categorias':categorias}
        return render(request,'inventario/categoriasEliminar.html', context,{})

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
    idCategoria = 0
    subCategorias = {}

    if(request.method == 'POST'):
        modificar = request.POST
        idCategoria = modificar.get('categoria')
        submitReq = modificar.get('productos-submit')

        subCategorias = {}
        if(idCategoria=='-1' or idCategoria==None):
            idCategoria = -1
            subCategorias = {}
        else:
            categoriaObject = Categoria.objects.get(pkCategoria=idCategoria)    
            subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)

        #CREAR REFERENCIAS ------------------------------------
        idSubCat = modificar.get('subCategoria')
        nombre = modificar.get('inputNombre')
        descripcion = modificar.get('DescrProducto')
        precio = 0
        iva = 0
        
        if(modificar.get('inputPrecio')!="" and modificar.get('inputPrecio')!=None):
            precio = int(modificar.get('inputPrecio'))    
        if(modificar.get('inputIva')!="" and modificar.get('inputIva')!=None):
            iva = int(modificar.get('inputIva'))*precio/100
        if(submitReq=="Crear Referencia" and not(idSubCat=="null") and not(nombre=="") and not(descripcion=="") and not(iva<=0) and not(precio<=0)):
            #print(imagen)
            imagen = request.FILES['buscadorImagen']#####
            aux = Producto(
                fkSubCategoria = SubCategoria.objects.get(pkSubCategoria=idSubCat),
                nombre = nombre,
                descripcion = descripcion,
                iva = iva,
                precio = precio,
                rutaImagen = imagen
            )
            aux.rutaImagen.save(imagen.name,File(imagen),'r')
            try:
                aux.full_clean()
            except ValidationError as e:
                context={'categorias':categorias, 'idCategoria':int(idCategoria), 'subCategorias':subCategorias}
                messages.info(request, 'Alguno(s) campo(s) no son validos')
                return render(request, "inventario/referenciasCrear.html", context, {})
            #aux.rutaImagen.save()
            aux.save()
            context={'categorias':categorias, 'idCategoria':int(idCategoria), 'subCategorias':subCategorias}
            messages.success(request, 'Referencia creada con exito')
            return render(request, "inventario/referenciasCrear.html", context, {})
        elif(submitReq=="Crear Producto"):
            context={'categorias':categorias, 'idCategoria':int(idCategoria), 'subCategorias':subCategorias}
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/referenciasCrear.html", context, {})

    context={'categorias':categorias, 'idCategoria':int(idCategoria), 'subCategorias':subCategorias}
    return render(request, "inventario/referenciasCrear.html", context, {})

def aniadirProductos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    bodegas = Bodega.objects.all()
    idCategoria = 0
    subCategorias = {}

    if(request.method == 'POST'):
        modificar = request.POST  
        submitReq = modificar.get('productos-submit')

        #AGREGAR PRODUCTOS ----------------------------------------------
        idProducto = modificar.get('producto')
        idProveedor = modificar.get('proveedor')
        idBodega = modificar.get('bodega')
        talla = modificar.get('talla')
        cantidad = 0
        if(modificar.get('inputCant')!="" and modificar.get('inputCant')!=None):
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

def modificarReferencias(request, *args, **kwargs):
    categorias = Categoria.objects.all()

    modificar = request.POST
    idcategoria = modificar.get('categoria')
    subcategorias = {}
    idsubcategoria = modificar.get('subcategoria')
    productos = {}
    idproducto = modificar.get('producto')
    catSeleccionada = False
    subCatSeleccionada = False
    producSeleccionado = False
    
    if((modificar.get('categoria') != "") and (modificar.get('categoria') != None) and (modificar.get('categoria') != "-1")):
        subcategorias = SubCategoria.objects.filter(fkCategoria=idcategoria)
        catSeleccionada = True
    else:
        idcategoria = -1

    if((modificar.get('subcategoria') != "") and (modificar.get('subcategoria') != None) and (modificar.get('subcategoria') != "-1")):
        productos = Producto.objects.filter(fkSubCategoria=idsubcategoria)
        subCatSeleccionada = True
    else:
        idsubcategoria = -1
    
    if((modificar.get('producto') != "") and (modificar.get('producto') != None) and (modificar.get('producto') != "-1")):                
        idproducto = modificar.get('producto')
        producSeleccionado = True
    else:
        idproducto = -1

    context={
        'categorias':categorias,
        'subcategorias':subcategorias, 
        'productos':productos,
        'idcategoria':int(idcategoria),
        'idsubcategoria':int(idsubcategoria),
        'idproducto':int(idproducto),
        'nombreO': "",
        'idO': "",
        'descripcionO': "",
        'ivaO': "",
        'precioO': "",
        'rutaImagenO': "",
    }

    if (modificar.get('productos-submit')=="Modificar Referencia"): #SE MODIFICA LA REFERENCIA
        nombre = modificar.get('inputNombre')
        descripcion = modificar.get('DescrProducto')
        precio = 0
        iva = 0
        if(modificar.get('inputPrecio')!="" and modificar.get('inputPrecio')!=None):
            precio = int(modificar.get('inputPrecio'))
        if(modificar.get('inputIva')!="" and modificar.get('inputIva')!=None):
            iva = int(modificar.get('inputIva'))*precio/100
        
        imagenModif = False
        idP = modificar.get('inputId')
        producObject = Producto.objects.get(pkProducto=idP)
        imagen = producObject.rutaImagen
        
        if((modificar.get('buscadorImagen')!= '')):
            imagen = request.FILES['buscadorImagen']
            imagenModif = True

        if(producSeleccionado and not(nombre=="") and not(descripcion=="") and not(iva<=0) and not(precio<=0) and not(imagen=="")): #catSeleccionada and subCatSeleccionada and 
            nombreCategoria = modificar.get('nombreCategoria')
            aux = Producto(                
                fkSubCategoria = SubCategoria.objects.get(pkSubCategoria=idsubcategoria),
                nombre = nombre,
                descripcion = descripcion,
                iva = iva,
                precio = precio,
                rutaImagen = imagen
            )
            #if(imagenModif):
                #save(imagen.name,File(imagen),'r')
            try:
                aux.full_clean()
            except ValidationError as e:
                messages.info(request, 'Alguno(s) campo(s) no son validos')
                context={
                    'categorias':categorias,
                    'subcategorias':subcategorias, 
                    'productos':productos,
                    'idcategoria':int(idcategoria),
                    'idsubcategoria':int(idsubcategoria),
                    'idproducto':int(idproducto),
                    'nombreO': aux.nombre,
                    'idO': int(modificar.get('inputId')),
                    'descripcionO': aux.descripcion,
                    'ivaO': modificar.get('inputIva'),
                    'precioO': aux.precio,
                    'rutaImagenO': "../"+imagen.name,
                }
                return render(request, "inventario/referenciasModificar.html", context, {})

            Producto.objects.filter(pkProducto = idproducto).update(
                                                                nombre = aux.nombre,
                                                                descripcion = aux.descripcion,
                                                                iva = aux.iva,
                                                                precio = aux.precio,
                                                                rutaImagen = aux.rutaImagen
                                                            )
            if(imagenModif):
                product = Producto.objects.get(pkProducto = idproducto)
                product.rutaImagen.save(imagen.name,File(imagen),'r')                
            messages.success(request, 'Referencia modificada exitosamente')
            context={
                'categorias':categorias,
                'subcategorias':subcategorias, 
                'productos':productos,
                'idcategoria':int(idcategoria),
                'idsubcategoria':int(idsubcategoria),
                'idproducto':int(idproducto),
                'nombreO': aux.nombre,
                'idO': int(modificar.get('inputId')),
                'descripcionO': aux.descripcion,
                'ivaO': modificar.get('inputIva'),
                'precioO': aux.precio,
                'rutaImagenO': "../"+imagen.name,
            }
            return render(request, "inventario/referenciasModificar.html", context, {})

        else:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            context={
                'categorias':categorias,
                'subcategorias':subcategorias, 
                'productos':productos,
                'idcategoria':int(idcategoria),
                'idsubcategoria':int(idsubcategoria),
                'idproducto':int(idproducto),
                'nombreO': nombre,
                'idO': int(modificar.get('inputId')),
                'descripcionO': descripcion,
                'ivaO': modificar.get('inputIva'),
                'precioO': precio,
                'rutaImagenO': "../"+imagen.name,
            }
            return render(request, "inventario/referenciasModificar.html", context, {})

    elif((idproducto != "") and (idproducto != None) and (idproducto != "-1") and (idproducto != -1)): #SE CARGAN LOS VALORES DE LA REFERENCIA
        producObject = Producto.objects.get(pkProducto=idproducto)
        nombreO = producObject.nombre
        descripcionO = producObject.descripcion        
        precioO = producObject.precio
        ivaOPorcent = producObject.iva
        ivaO = int(math.ceil((ivaOPorcent*100)/precioO))
        rutaImagenO = producObject.rutaImagen

        context={
            'categorias':categorias,
            'subcategorias':subcategorias, 
            'productos':productos,
            'idcategoria':int(idcategoria),
            'idsubcategoria':int(idsubcategoria),
            'idproducto':int(idproducto),
            'nombreO': nombreO,
            'idO': int(idproducto),
            'descripcionO': descripcionO,
            'ivaO': ivaO,
            'precioO': precioO,
            'rutaImagenO': "../"+rutaImagenO.name,
        }
    return render(request, "inventario/referenciasModificar.html", context, {})

def modificarProductos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    idProducto = 0
    proveedores = Proveedor.objects.all()
    idProveedor = 0
    bodegas = Bodega.objects.all()
    idBodega = 0

    detalles = {}
    idDetalle = 0

    #Variables de carga de campos
    referenciaO = ""
    idrefO= 0
    tallaO = ""
    nitO = ""
    colorO = ""
    fkBodegaO = ""
    cantidadO = 0

    if(request.method == 'POST'):
        modificar = request.POST
        #if((modificar.get('producto') != None) and (modificar.get('producto') != "") and (modificar.get('producto') != "-1")):
        idProducto = int(modificar.get('producto'))
        idProveedor = modificar.get('proveedor')
        idBodega = int(modificar.get('bodega'))

        #BUSCAR DETALLES
        if((idProducto!=-1) and (idProveedor!="-1") and (idBodega!=-1)): #LOS TRES CAMPOS SELECCIONADOS
            detalles = DetallesProducto.objects.filter(fkProducto=idProducto,
                                                        nit=idProveedor,
                                                        fkBodega=idBodega)
        elif((idProducto!=-1) and (idProveedor!="-1")):  #PRODUCTO Y PROVEEDOR SELECCIONADOS
            detalles = DetallesProducto.objects.filter(fkProducto=idProducto,
                                                        nit=idProveedor)
        elif((idProducto!=-1) and (idBodega!=-1)):     #PRODUCTO Y BODEGA SELECCIONADOS
            detalles = DetallesProducto.objects.filter(fkProducto=idProducto,
                                                        fkBodega=idBodega)
        elif((idProveedor!="-1") and (idBodega!=-1)):    #PROVEEDOR Y BODEGA SELECCIONADOS
            detalles = DetallesProducto.objects.filter(nit=idProveedor,
                                                        fkBodega=idBodega)
        else: #SOLO UN CAMPO SELECC
            if(idProducto!=-1):    #PRODUCTO SELECCIONADO
                detalles = DetallesProducto.objects.filter(fkProducto=idProducto)
            elif(idProveedor!="-1"): #PROVEEDOR SELECCIONADO
                detalles = DetallesProducto.objects.filter(nit=idProveedor)
            elif(idBodega!=-1):    #BODEGA SELECCIONADA
                detalles = DetallesProducto.objects.filter(fkBodega=idBodega)


        #MODIFICAR EL PRODUCTO
        if((modificar.get('productos-submit')=="Modificar Producto") and (modificar.get('detalle') != None) and (modificar.get('detalle') != "") and (modificar.get('detalle') != "-1")):
            idDetalle = int(modificar.get('detalle'))

            referencia = int(modificar.get('idref'))
            talla = modificar.get('inputTalla')
            nit = modificar.get('inputProveedor')
            color = modificar.get('inputColor')
            PkBodega = int(modificar.get('inputBodega'))
            cantidad = int(modificar.get('inputCant'))

            aux = DetallesProducto(
                fkProducto = Producto.objects.get(pkProducto=referencia),
                talla = talla,
                nit = Proveedor.objects.get(pknit=nit),
                color = color,
                fkBodega = Bodega.objects.get(pkBodega=PkBodega),
                cantidad = cantidad
            )
            try:
                aux.full_clean()
            except ValidationError as e:
                print(e)
                messages.info(request, 'Cantidad invalida')
                context={'categorias':categorias, 'productos':productos, 'idProducto':idProducto, 'proveedores':proveedores, 'idProveedor':idProveedor, 'bodegas':bodegas, 'idBodega':idBodega, 'detalles':detalles, 'idDetalle':idDetalle, 'referencia':aux.fkProducto.nombre, 'idref':aux.fkProducto.pkProducto, 'talla':talla, 'nit':nit, 'color':color, 'pkBodega':PkBodega, 'cantidad':cantidad}
                return render(request, "inventario/productosModificar.html",context, {})

            DetallesProducto.objects.filter(pkDetallesP = idDetalle).update(cantidad = aux.cantidad)

            messages.success(request, 'Producto modificado exitosamente')
            context={'categorias':categorias, 'productos':productos, 'idProducto':idProducto, 'proveedores':proveedores, 'idProveedor':idProveedor, 'bodegas':bodegas, 'idBodega':idBodega, 'detalles':detalles, 'idDetalle':idDetalle, 'referencia':aux.fkProducto.nombre, 'idref':aux.fkProducto.pkProducto, 'talla':aux.talla, 'nit':nit, 'color':aux.color, 'pkBodega':PkBodega, 'cantidad':aux.cantidad}
            return render(request, "inventario/productosModificar.html",context, {})

        #OBTENER LOS CAMPOS ANTIGUOS
        elif((modificar.get('detalle') != None) and (modificar.get('detalle') != "") and (modificar.get('detalle') != "-1")):
            idDetalle = int(modificar.get('detalle'))
            print(idDetalle)
            detalleObject = DetallesProducto.objects.get(pkDetallesP=idDetalle)
            
            referenciaO = detalleObject.fkProducto.nombre
            idrefO = detalleObject.fkProducto.pkProducto
            tallaO = detalleObject.talla
            nitO = detalleObject.nit.pknit
            colorO = detalleObject.color
            fkBodegaO = detalleObject.fkBodega.pkBodega
            cantidadO = detalleObject.cantidad

    context={'categorias':categorias, 'productos':productos, 'idProducto':idProducto, 'proveedores':proveedores, 'idProveedor':idProveedor, 'bodegas':bodegas, 'idBodega':idBodega, 'detalles':detalles, 'idDetalle':idDetalle, 'referencia':referenciaO, 'idref':idrefO, 'talla':tallaO, 'nit':nitO, 'color':colorO, 'pkBodega':fkBodegaO, 'cantidad':cantidadO}
    #print(context)
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





def modificarProveedor(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    context={'categorias': categorias, 'proveedores': proveedores, 'nit': '', 'telefono': '', 'direccion': ''}
    modificar = request.POST
    nit = modificar.get('nitProveedor')
    actualNit = modificar.get('nit')
    acccionModProveedorSubmit = modificar.get('modificarProveedor-submit')

    #Seleccionar el primer proveedor con el nit si existe
    objectProveedor = Proveedor.objects.filter(pknit = nit).first()
    
    if ( acccionModProveedorSubmit == "Modificar"):
        if (actualNit == ''):
            messages.info(request, 'Seleccione el NIT del proveedor que desea actualizar')
            return render(request, "inventario/proveedorModificar.html",context,{})
        
        telefonoNuevo = modificar.get('telefonoProveedor')
        direccionNueva = modificar.get('direccionProveedor')
        
        
        aux = Proveedor( pknit = actualNit, direccion = direccionNueva, telefono = telefonoNuevo)
        
        try:
            #No se puede full_clean debido a que no seria una clave unica en el modelo su nit
            aux.clean_fields()
            aux.clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "inventario/proveedorModificar.html",context,{})
        Proveedor.objects.filter(pknit = actualNit).update(direccion=direccionNueva, telefono = telefonoNuevo)
        messages.success(request, 'El proveedor ha sido actualizado correctamente')
        return render(request, "inventario/proveedorModificar.html",context,{})

    if (nit != "no elegido" and nit != None):
        telefono = objectProveedor.telefono
        direccion = objectProveedor.direccion
    else:
        nit = ''
        telefono = ''
        direccion = ''
    context={'categorias': categorias, 'proveedores': proveedores, 'nit': nit, 'telefono': telefono, 'direccion': direccion}
    
    return render(request, "inventario/proveedorModificar.html", context, {})

def productosCategoriasVista(request, nombre, categoria):
    categorias = Categoria.objects.all()
    subCategorias=SubCategoria.objects.filter(fkCategoria=categoria)
    context={'categorias':categorias, 'subCategorias':subCategorias, 'categoria':categoria, 'nombre':nombre}
    return render(request, 'inventario/productoCategoriaVista.html', context, {})

def productosSubCategoriasVista(request, nombre, categoria ,subCategoria):
    categorias = Categoria.objects.all()
    subCategorias= SubCategoria.objects.filter(fkCategoria=categoria)
    productos=Producto.objects.filter(fkSubCategoria=subCategoria)
    context={'categorias':categorias, 'subCategorias':subCategorias, 'productos': productos, 'categoria':categoria, 'nombre':nombre}
    return render(request, 'inventario/productoCategoriaVista.html', context, {})


def modificarBodega(request):
    categorias = Categoria.objects.all()
    bodegas = Bodega.objects.all()
    modificar = request.POST
    idBodega = modificar.get('bodega')
    bodegaSeleccionada = False

    if(idBodega=='-1' or idBodega==None):
        ciudadBodega = ""
        dirBodega = ""
    else:
        BodegaObject = Bodega.objects.get(pkBodega=idBodega)
        ciudadBodega = BodegaObject.ciudad
        dirBodega = BodegaObject.direccion
        ciudadB = modificar.get('ciudad')
        dirB = modificar.get('direccion')
                    
        aux =  Bodega(direccion =dirB, ciudad = ciudadB)
        
        if(modificar.get('modfBod-submit')!= None):
            try:
                aux.full_clean()
            except ValidationError as e:
                context={'categorias':categorias, 'bodegas':bodegas, 'ciudadBodega':ciudadBodega, 'dirBodega':dirBodega}
                messages.info(request, 'Datos invalidos')
                return render(request, "inventario/bodegaModificar.html", context, {})

            Bodega.objects.filter(pkBodega=idBodega).update(ciudad= aux.ciudad, direccion=aux.direccion)
            context={'categorias':categorias, 'bodegas':bodegas, 'ciudadBodega':ciudadB, 'dirBodega':dirB} 
            messages.info(request, 'Bodega modificada correctamente')   
            return render(request, 'inventario/bodegaModificar.html', context, {})


    context={'categorias':categorias, 'bodegas':bodegas, 'ciudadBodega':ciudadBodega, 'dirBodega':dirBodega}
    return render(request, "inventario/bodegaModificar.html", context, {})

