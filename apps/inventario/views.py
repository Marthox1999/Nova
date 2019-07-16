from django.shortcuts import render
from django.http import HttpResponse
from inventario.models import Categoria, SubCategoria
# Create your views here.

def modificar_categoria(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    modificar = request.POST  
    idCategoria = modificar.get('categoria')
    subCategorias = {}
    if(idCategoria=='-1'):
        print("entro")
        subCategorias = {}
    else:
        subCategorias = SubCategoria.objects.filter(fkCategoria=idCategoria)

    context={'categorias':categorias, 'subCategorias':subCategorias}
    return render(request, "inventario/modificar_categoria.html", context, {})

def prueba(request, *args, **kwargs):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    print(request.POST)
    return render(request, "prueba.html", context, {})
    