from django.shortcuts import render

from ventas.models import *
from datetime import timedelta, date, datetime

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def reporteVentas(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        data = request.POST
        fechaInicio = datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d')
        fechaFin = datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d')
        dias = []
        cantidad = []
        for dia in daterange(fechaInicio, fechaFin):
            cant = Factura.objects.filter(fecha=dia).count()
            cantidad.append(cant)
            dias.append(dia.strftime('%Y-%m-%d'))
        context={"datax":dias,"datay":cantidad}
        print(len(dias), len(cantidad))
        return render(request, "reportes/reporteVentas.html", context, {})
    
    return render (request, "reportes/reporteVentas.html", context, {})