
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ValidationError
from django.utils import timezone
from usuarios.models import *
from inventario.models import Categoria

from django.db import transaction

def clienteIngreso(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    ingresar = request.POST
    context={'categorias':categorias, 'nombre':'noRegistrado'}
    if(request.method == 'POST'):
        aux = Cliente(
            nombre=ingresar.get('username'),
            clave=ingresar.get('password'),
            fechaNacimiento = timezone.now,
            direccion = "",
            telefono = "",
            tipoDocumento = "",
            numeroDocumento = 1234567,
        )
        nombre=ingresar.get('username')
        if (aux.autenticarCliente()):
            context={'categorias':categorias, 'nombre':nombre}
            messages.success(request, f'¡Bienvenido {nombre}!')
            return render(request, 'usuarios/clienteinicio.html', context,{})
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/clienteingreso.html', context,{'form':ingresar})

def clienteCerrarSesion(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, 'usuarios/clienteingreso.html', context, {})

def clienteInicio(request, nombre):
    categorias = Categoria.objects.all()
    context={'categorias':categorias, 'nombre': nombre}
    return render(request, 'usuarios/clienteinicio.html', context, {})

@csrf_protect
def clienteregistro(request):
    categorias = Categoria.objects.all()
    context={'categorias':categorias, 'nombre':'noRegistrado'}
    registrar = request.POST
    if(request.method == 'POST'):
        aux = Cliente(
            nombre= registrar.get('nombreCliente'),
            clave = registrar.get('claveCliente'),
            fechaNacimiento = registrar.get('fechaNacimiento'),
            direccion = registrar.get('direccionCliente'),
            telefono = registrar.get('telefonoCliente'),
            tipoDocumento = registrar.get('tipoDocumento'),
            numeroDocumento = registrar.get('documentoCliente'),
        )
        try:
            aux.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "usuarios/clienteregistro.html", context,{'form':registrar})
        nombre =registrar.get('nombreCliente')
        aux.save()
        messages.success(request, f'¡{nombre} bienvenido(a) a Nova!')
        return render(request, 'usuarios/clienteingreso.html', context,{})
    return render(request, "usuarios/clienteregistro.html",context, {'form':registrar})


def paginaPrincipal_admin(request):
    categorias = Categoria.objects.all()
    admin = AdministradorDuenio.objects.get(pkAdministradorDuenio =  1)
    #admin = get_object_or_404(AdministradorDuenio, pkAdministradorDuenio=id_dueno)
    context = {
        'objeto' : admin,
        'categorias': categorias
    }
    return render(request, "usuarios/paginaPrincipal_admin.html",context)

def paginaPrincipal_duenio(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    duenio = AdministradorDuenio.objects.get(pkAdministradorDuenio=1)
    context = {
        'objeto' : duenio,
        'categorias': categorias
    }
    return render(request, "usuarios/paginaPrincipal_duenio.html",context)


def duenioAdminAgregar(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    agregar = request.POST
    if(request.method=='POST'):
        admin=AdministradorDuenio(
            nombreUsuario=agregar.get('nombreAdmin'),
            clave=agregar.get('claveAdmin'),
            tipo='ADMIN'
        )
        try:
            admin.full_clean()
        except ValidationError as e:
            messages.info(request, 'Alguno(s) campo(s) no son validos')
            return render(request, "usuarios/duenioAdminAgregar.html",context,{'form':agregar})
        nombre =agregar.get('nombreAdmin')
        admin.save()
        messages.success(request, f'¡Bienvenido {nombre} !')
        return redirect(to='usuarios:duenioAgregarAdmin')
    return render(request,"usuarios/duenioAdminAgregar.html",context,{'form':agregar})


def adminMenu(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request,"usuarios/adminMenu.html",context, {})


def clienteMenu(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    return render(request,"usuarios/clienteMenu.html",context, {})


def duenioAdminIngreso(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    ingresar = request.POST
    if(request.method == 'POST'):
        admin = AdministradorDuenio(
            nombreUsuario=ingresar.get('nombreDuenioAdmin'),
            clave=ingresar.get('claveDuenioAdmin'),
            tipo='ADMIN'
        )

        duenio=AdministradorDuenio(
            nombreUsuario=ingresar.get('nombreDuenioAdmin'),
            clave=ingresar.get('claveDuenioAdmin'),
            tipo='CEO'
        )
        nombre=ingresar.get('nombreDuenioAdmin')
        if (admin.autenticarAdmin()):
            messages.success(request, f'¡Bienvenido {nombre}!')
            return redirect(to='usuarios:paginaPrincipal_admin')
        elif (duenio.autenticarDuenio()):
            messages.success(request, f'¡Bienvenido {nombre}!')
            return redirect(to='usuarios:paginaPrincipal_duenio')
        else:
            messages.info(request, 'Cuenta de usuario o contraseña invalida')
    return render(request, 'usuarios/duenioAdminIngreso.html',context,{'form':ingresar})

def duenioAdminModificar(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    usuarios = AdministradorDuenio.objects.filter(tipo='ADMIN')
    context={'categorias':categorias, 'usuarios':usuarios}

    modificar = request.POST
    
    nombreAdmin = modificar.get('nombreEmpleado')
    claveAdmin = modificar.get('claveAdmin')

    if(request.method == 'POST'):
        try:
            print ('Llega a antes de modificar')
            objects = AdministradorDuenio.objects.filter(nombreUsuario = nombreAdmin)
            #Hice la modificación de la clave como atributo para usar save
            #y asi usar el encriptado dentro de la función, en lugar de usar update
            for obj in objects:
                obj.clave = claveAdmin
                obj.save()
            
            messages.success(request, 'Administrador modificado exitosamente')
        except ValidationError as e:
            messages.info(request, 'El usuario administrador no pudo ser modificado')
            
    return render(request, "usuarios/duenioAdminModificar.html", context, {})
    
def duenioClienteConsultar(request, *args, **kwargs):
    from django.db.models import Q
    categorias = Categoria.objects.all()
    clientes = {}
    consultar = request.POST
    buscador = consultar.get('buscador')
    if (buscador):
        clientes = Cliente.objects.filter(Q(nombre__icontains=buscador) | Q(direccion__icontains=buscador) | Q(telefono__icontains=buscador) | Q(numeroDocumento__icontains=buscador))
    else:
        clientes = Cliente.objects.all()
    context={'categorias':categorias, 'clientes': clientes}
        
    return render(request, "usuarios/duenioClienteConsultar.html", context, {})


def clientePerfil(request, nombre):
    cliente = Cliente.objects.filter(nombre=nombre)
    context = {'nombre':nombre, 'cliente':cliente}
    return render(request,"usuarios/clientePerfil.html", context, {})



def clienteCarrito(request, nombre):
    import datetime
    from ventas.models import PagosDebito, PagosCredito, DetallesFactura, Factura
    categorias = Categoria.objects.all()
    accion = request.POST
    print(accion)
    idEliminar = accion.get('eliminar')
    numTarjetas = accion.get('cuantas')
    tipoTarjeta = accion.get('tipotarjeta')
    #subtotal de productos en carrito
    productosCarrito = Carrito.objects.filter(fkNombreCliente=nombre)
    totalcompra = 0
    cantidadValida = False
    num = {}
    for producto in productosCarrito:
        totalcompra += (producto.precioActual *  producto.cantidad)
    #eliminar producto
    if(idEliminar):
        try:
            Carrito.objects.filter(pkCarrito=idEliminar).delete()
        except ValidationError as e:
            messages.info(request, 'El artículo no pudo ser eliminado del carrito')
    #compra transaccional
    #cantidad de tarjetas a utilizar 1, 2 o 3
    with transaction.atomic():
        if(numTarjetas):
            try:
                num = range(1, int(numTarjetas)+1)
            except ValidationError as e:
                messages.info(request, 'Error para identificar la cantidad de tarjetas')
            except ValueError as e:
                pass
                #Significa que uno de los campos no fue llenado pero no es necesario informar, porque pudo ser aproposito si solo se usa un medio de pago
        #tipos de tarjetas
        numeroDebito = accion.get('cuantasDebito')
        cuantasDebito = {}
        numeroCredito = accion.get('cuantasCredito')
        cuantasCredito = {}
        if(numeroDebito or numeroCredito):
            try:
                if(( int(numeroDebito) + int(numeroCredito) > 3) or (int(numeroCredito) + int(numeroDebito) == 0)):
                    messages.info(request, 'Error puede usar maximo 3 tarjetas y minimo 1 tarjeta')    
                else:
                    cantidadValida = True
                    cuantasDebito = range(1, int(numeroDebito)+1)
                    cuantasCredito = range(1, int(numeroCredito)+1)
            except ValidationError as e:
                messages.info(request, 'Error para identificar la cantidad de tarjetas')
                context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
                return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})
                #Significa que uno de los campos no fue llenado pero no es necesario informar, porque pudo ser aproposito si solo se usa un medio de pago
        
        #recolectando info de tarjetas y destino
        numDebito = accion.getlist('numDebito')
        numCredito = accion.getlist('CnumTarjeta')
        if(numDebito or numCredito):
            if (len(numDebito) + len(numCredito) > 3):
                messages.info(request, 'Error maximo puede usar 3 tarjetas')
            else:
                Dporcentaje = accion.getlist('Dporcentaje')
                Cporcentaje = accion.getlist('Cporcentaje')
                sumd = sumc = 0
                #acumular porcentajes de tarjetas
                try:
                    for dp in Dporcentaje:
                        sumd += int(dp)
                    for dc in Cporcentaje:
                        sumc += int(dc)
                except ValueError as e:
                    messages.info(request, 'No agrego porcentajes de pago validos')
                    context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
                    return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})
                #porcentajes que sumen 100
                if(sumd + sumc  != 100):
                    messages.info(request, 'Error, no se a asignado el total de la venta en los porcentajes de las tarjetas')
                else:
                    #haber seleccionado entidades
                    entidades = accion.getlist('entidad')
                    for e in entidades:
                        if(e == '-1'):
                            messages.info(request, 'Error, no se selecciono una entidad valida')
                            break
                    #atrapar toda la informacion para crear las tarjetas
                    Dahorros = accion.getlist('Dahorros')
                    CnumAprobacion = accion.getlist('CnumAprobacion')
                    direccion = accion.get('direccion')
                    ciudad = accion.get('ciudad')
                    cuotas = accion.get('Ccuotas')
                    hoy =datetime.date.today()
                    #crear factura general
                    auxCliente = Cliente.objects.get(nombre = nombre)
                    auxFactura = Factura(fkCliente = auxCliente, ciudad = ciudad, direccion = direccion, fecha = hoy)
                    try:   
                        auxFactura.full_clean() #
                    except ValidationError as e:
                        messages.info(request, 'Error para la creación de la factura')
                        context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
                        return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})
                    auxFactura.save()
                    print("factura guardada")
                    print(productosCarrito)
                    #crear detalles de factura uno por producto en carrito
                    for item in productosCarrito:
                        print(item)
                        auxDetalleproducto = DetallesProducto.objects.get(pkDetallesP = item.fkDetalleProducto.pkDetallesP)
                        auxDetalleFactura = DetallesFactura(fkFactura = auxFactura,
                                                            fkDetallesProducto = item.fkDetalleProducto,
                                                            cantidad = item.cantidad,
                                                            precio = item.precioActual)
                        try:   
                            auxDetalleFactura.full_clean()
                        except ValidationError as e:
                            messages.info(request, 'Error para productos asociados a la venta')
                            context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
                            return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})
                        auxDetalleFactura.save()
                    #crear tarjetas usadas
                    #tarjetas debito
                    count = 0
                    for d in numDebito:
                        auxahorro = False
                        if (Dahorros == 'on'):
                            auxahorro = True
                        auxDebito = PagosDebito(numeroTarjetaDebito = d,
                                                fkFactura = auxFactura,
                                                porcentajePago = Dporcentaje[count],
                                                ahorros = auxahorro)
                        try:   
                            auxDebito.full_clean()
                        except ValidationError as e:
                            print(str(e))
                            messages.info(request, 'Error en los datos de la(s) tarjeta(s) de debito')
                            context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
                            return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})
                        auxDebito.save()
                        count+=1
                    print("falta credito pero se creo la debito")
                    #tarjetas credito
                    count = 0
                    for c in numCredito:
                        auxCredito = PagosCredito(fkFactura = auxFactura,
                                                  numeroAprobacion = CnumAprobacion,
                                                  cuotas = cuotas,
                                                  fechaAprobacion = hoy,
                                                  entidadAprobacion = entidades[count],
                                                  porcentajePago = Cporcentaje[count])
                        try:
                            auxCredito.full_clean()
                        except ValidationError as e:
                            print(str(e))
                            messages.info(request, 'Error en los datos de la(s) tarjeta(s) de credito')
                        auxCredito.save()
                        count += 1
                    #restar del inventario
                    for item in productosCarrito:
                        auxcantidad = item.cantidad
                        DetallesProducto.objects.filter(pkDetallesP = item.fkDetalleProducto.pkDetallesP).update(cantidad = item.fkDetalleProducto.cantidad  - auxcantidad)
                    #vaciar el carrito
                    
                    Carrito.objects.filter(fkNombreCliente = auxCliente).delete() #elimino los items en carrito
                    #si todo salio bien
                    messages.success(request, 'Compra realizada exitosamente')

    context = {'cantidadValida': cantidadValida, 'totalcompra':totalcompra,'categorias':categorias,'nombre': nombre, 'productosCarrito': productosCarrito, 'rangeDebito': cuantasDebito, 'numtarjetas':num, 'numeroDebito': numeroDebito, 'rangeCredito': cuantasCredito, 'numeroCredito': numeroCredito}
    return render(request, "usuarios/clienteCarrito.html", context, {'form':accion})

