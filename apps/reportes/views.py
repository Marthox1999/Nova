from django.shortcuts import render, redirect
from django.contrib import messages

from ventas.models import *
from datetime import timedelta, date, datetime
from django.db.models import Sum

def inicioReportes(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        data = request.POST
        print(data)
        reporte = data.get('tipoReporte')
        url = 'reportes:'+reporte
        return redirect(to=url)
    return render (request, "reportes/reportes.html", context, {})

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def reporteVentas(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        data = request.POST
        fechaInicio = ""
        fechaFin = ""
        try:
            fechaInicio = datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d')
            fechaFin = datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d')
        except:
            messages.info(request, 'Por favor ingrese una fecha valida')
            return render(request, "reportes/reporteVentas.html", context, {})
        dias = []
        cantidad = []
        for dia in daterange(fechaInicio, fechaFin):
            cant = Factura.objects.filter(fecha=dia).count()
            cantidad.append(cant)
            dias.append(dia.strftime('%Y-%m-%d'))
        context={"datax":dias,"datay":cantidad, "fechaInicio":fechaInicio.strftime('%Y-%m-%d'), "fechaFin":fechaFin.strftime('%Y-%m-%d')}
        return render(request, "reportes/reporteVentas.html", context, {})
    
    return render (request, "reportes/reporteVentas.html", context, {})

def reporteVentasCategoria(request, *args, **kwargs):
    context = {}
            
    cats = Categoria.objects.all()
    categorias = []
    cantidades = []

    for p in cats:
        categorias.append(p.nombreCategoria)
        cant = 0

        subCats = SubCategoria.objects.filter(fkCategoria=p.pkCategoria)

        for subC in subCats:
            productos = Producto.objects.filter(fkSubCategoria=subC.pkSubCategoria)

            for product in productos:
                detalles = DetallesProducto.objects.filter(fkProducto=product.pkProducto)

                for deta in detalles:
                    detallesFacturas = DetallesFactura.objects.filter(fkDetallesP=deta.pkDetallesP)

                    for detaFact in detallesFacturas:
                        cant = cant + detaFact.cantidad

        cantidades.append(cant)

    context={"datax":categorias,"datay":cantidades}

    if(categorias == []):
        messages.info(request, 'No hay categorías')

    print(context)
    
    return render (request, "reportes/reporteVentasCategoria.html", context, {})


def insertionSort(arr): 
  
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
        key = arr[i] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and key[2] > arr[j][2] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key

    return arr 

def reporteTopClientes(request, *args, **kwargs):
    top = 0
    clientesTop = []    
    clientesTopFinal = []

    if request.method == 'POST':
        datos = request.POST
        topStr = datos.get('top')

        if((topStr!='') and (topStr!=None) and (int(topStr)>0)):
            top = int(topStr)
            clientes = Cliente.objects.all()
            numClientes = clientes.count()

            #Consigue una lista de los clientes con su respectiva cantidad de productos comprada y dinero invertido
            for cliente in clientes:
                totalC = 0
                totalV = 0
                
                facturas = Factura.objects.filter(fkCliente=cliente.nombre)

                for factura in facturas:
                    detalleFactura = DetallesFactura.objects.filter(fkFactura=factura.pkFactura).annotate(totalC=Sum('cantidad'),totalV=Sum('precio'))    

                    if(not(detalleFactura.exists())):
                        continue
                        
                    totalC = totalC + detalleFactura[0].totalC
                    totalV = totalV + detalleFactura[0].totalV
                            
                if(totalC!=0):
                    clientesTop.append([cliente.nombre,totalC,totalV])                
            

            clientesTop = insertionSort(clientesTop) #Organiza la lista del top de mayor a menor

            if(top>numClientes):
                messages.info(request,'Hay menos clientes registrados de los indicados')

            conteo = 0
            conteoTop = top
            if(top>len(clientesTop)):
                conteoTop = len(clientesTop)
                messages.info(request,'Los clientes sin compras son omitidos')
            elif(top>numClientes): conteoTop = numClientes

            #Acomoda la lista del top en el formato para el html
            for Ctop in clientesTop:
                if(Ctop[1]==0):
                    continue

                if(conteo>=conteoTop):
                    break

                clientesTopFinal.append({'nombre':Ctop[0],'cantidad':Ctop[1],'dinero':Ctop[2]})
                conteo = conteo + 1

        else:
            messages.info(request, 'Por favor ingrese una cantidad válida')
        
    context = {'top':top, 'clientes':clientesTopFinal}
    return render (request, "reportes/reporteTopClientes.html", context, {})