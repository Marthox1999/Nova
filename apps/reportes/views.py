from django.shortcuts import render, redirect
from django.contrib import messages

from ventas.models import *
from datetime import timedelta, date, datetime

def inicioReportes(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        data = request.POST
        print(data)
        reporte = data.get('tipoReporte')
        url = 'reportes:'+reporte
        if(reporte == '1'):
            return redirect(to='reportes:reporteVentas')
        else:
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