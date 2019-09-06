from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum
from ventas.models import *
from datetime import timedelta, date, datetime
from inventario.models import *

# Create your views here.

def masVendidos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    
    productos = DetallesFactura.objects.values('fkDetallesP__fkProducto__fkSubCategoria__nombreSubCategoria', 'fkDetallesP__fkProducto__fkSubCategoria__fkCategoria__nombreCategoria', 'fkDetallesP__fkProducto__pkProducto', 'fkDetallesP__fkProducto__nombre').annotate(total=Sum('cantidad')).order_by('-total')[:20]
    
    context={'categorias':categorias, 'productos': productos, 'masOMenos': 'Más'}
    return render(request, 'reportes/vendidos.html', context, {})

    

def menosVendidos(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    
    productos = DetallesFactura.objects.values('fkDetallesP__fkProducto__fkSubCategoria__nombreSubCategoria', 'fkDetallesP__fkProducto__fkSubCategoria__fkCategoria__nombreCategoria', 'fkDetallesP__fkProducto__pkProducto', 'fkDetallesP__fkProducto__nombre').annotate(total=Sum('cantidad')).order_by('total')[:20]
    
    context={'categorias':categorias, 'productos': productos, 'masOMenos': 'Menos'}
    return render(request, 'reportes/vendidos.html', context, {})



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

def reportePocasUnidades(request):
    categorias = Categoria.objects.all()
    ingresar = request.POST

    productos = DetallesProducto.objects.values('fkProducto__nombre', 'color', 'talla').annotate(total=Sum('cantidad')).filter(total__lte=5)
    print(productos.query)
    print(productos)
    
    context={'categorias':categorias, 'productos': productos}
    return render(request, 'reportes/reportePocasUnidades.html', context, {})
   

