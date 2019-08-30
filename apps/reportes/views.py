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
        if(reporte == '1'):
            return redirect(to='reportes:reporteVentas')
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