from django.shortcuts import render, redirect
from django.contrib import messages
from ventas.models import *
from datetime import timedelta, date, datetime
from django.db.models import Sum
from inventario.models import *

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

def reportePocasUnidades(request):
    categorias = Categoria.objects.all()
    ingresar = request.POST

    productos = DetallesProducto.objects.values('fkProducto__nombre', 'color', 'talla').annotate(total=Sum('cantidad')).filter(total__lte=5)
    print(productos.query)
    print(productos)
    
    context={'categorias':categorias, 'productos': productos}
    return render(request, 'reportes/reportePocasUnidades.html', context, {})
   