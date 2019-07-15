from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from inventario.models import Bodega

@csrf_protect
def bodegaRegistro(request, *args, **kwargs):
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
            return render(request,'inventario/bodegaregistro.html',{'form':crearBodega})
        bodega.save()
        messages.success(request, 'La bodega ha sido creada correctamente')
        return redirect(to='registro')
    return render(request, 'inventario/bodegaregistro.html',{'form':crearBodega})
