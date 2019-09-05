from django.shortcuts import render, redirect
from django.contrib import messages

from ventas.models import *
from datetime import timedelta, date, datetime
from dateutil import relativedelta

def inicioReportes(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        data = request.POST
        reporte = data.get('tipoReporte')
        url = "reportes:"+reporte
        return redirect(to=url)
    return render (request, "reportes/reportes.html", context, {})

def daterangeday(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def daterangemonth(start_date, end_date):
    r = relativedelta.relativedelta(end_date, start_date).months
    for n in range(r):
        yield start_date + relativedelta.relativedelta(months=+n)

def daterangeyear(start_date, end_date):
    r = relativedelta.relativedelta(end_date, start_date).years
    for n in range(r):
        yield start_date + relativedelta.relativedelta(years=+n)

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
        tipoReporte = int(data.get('tipoReporte'))
        dias = []
        cantidad = []
        if (tipoReporte==1):
            cant = 0
            for dia in daterangeday(fechaInicio, fechaFin):
                cant = Factura.objects.filter(fecha=dia).count()
                cantidad.append(cant)
                dias.append(dia.strftime('%Y-%m-%d'))
            context={"datax":dias,"datay":cantidad, "fechaInicio":fechaInicio.strftime('%Y-%m-%d'), "fechaFin":fechaFin.strftime('%Y-%m-%d')}
            return render(request, "reportes/reporteVentas.html", context, {})
        if (tipoReporte==2):
            fechaInicio = date(fechaInicio.year, fechaInicio.month, 1)
            fechaFin = date(fechaFin.year, fechaFin.month, 1)
            for mes in daterangemonth(fechaInicio, fechaFin):
                cant = 0
                for dia in daterangeday(mes, (mes + relativedelta.relativedelta(months=+1)) ):
                    cant += Factura.objects.filter(fecha=dia).count()
                cantidad.append(cant)
                dias.append(mes.strftime('%Y-%m'))
            context={"datax":dias,"datay":cantidad, "fechaInicio":fechaInicio.strftime('%Y-%m'), "fechaFin":fechaFin.strftime('%Y-%m')}
            return render(request, "reportes/reporteVentas.html", context, {})
        if (tipoReporte==3):
            fechaInicio = date(fechaInicio.year, 1, 1)
            fechaFin = date(fechaFin.year, 1, 1) + relativedelta.relativedelta(years=+1)
            for year in daterangeyear(fechaInicio, fechaFin):
                cant = 0
                for dia in daterangeday(year, (year + relativedelta.relativedelta(years=+1)) ):
                    cant += Factura.objects.filter(fecha=dia).count()
                cantidad.append(cant)
                dias.append(year.strftime('%Y'))
            context={"datax":dias,"datay":cantidad, "fechaInicio":fechaInicio.strftime('%Y'), "fechaFin":fechaFin.strftime('%Y')}
            return render(request, "reportes/reporteVentas.html", context, {})

    return render (request, "reportes/reporteVentas.html", context, {})

def reporteProducto(request, *args, **kwargs):
    from django.db.models import Q
    productos = Producto.objects.all()
    context = {'productos':productos}
    if request.method == 'POST':
        data = request.POST
        today = date.today()
        fechaFin = date(today.year, today.month, today.day)
        fechaInicio = fechaFin + relativedelta.relativedelta(months=-6)
        try:
            producto = int(data.get('producto'))
        except:
            messages.info(request, 'Por favor seleccione un producto')
            return render(request, "reportes/reporteProducto.html", context, {})
        dias = []
        cantidad = []
        prod = Producto.objects.get(pkProducto=producto)
        for dia in daterangeday(fechaInicio, fechaFin):
            cant = 0
            facturas = Factura.objects.filter(fecha=dia)
            for factura in facturas:
                cant += DetallesFactura.objects.filter(Q(fkProducto=producto) & Q(fkFactura=factura.pkFactura)).count()
            cantidad.append(cant)
            dias.append(dia.strftime('%Y-%m-%d'))
        context={'productos':productos, "datax":dias,"datay":cantidad, "fechaInicio":fechaInicio.strftime('%Y-%m-%d'), "fechaFin":fechaFin.strftime('%Y-%m-%d'), 'producto':prod}
        return render(request, "reportes/reporteProducto.html", context, {})

    return render (request, "reportes/reporteProducto.html", context, {})