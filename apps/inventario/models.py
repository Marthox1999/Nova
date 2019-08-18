from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

#Categoria
class Categoria(models.Model):
    pkCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=256, unique=True)

#Subcategoria
class SubCategoria(models.Model):
    pkSubCategoria = models.AutoField(primary_key=True)
    fkCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombreSubCategoria = models.CharField(max_length=256, unique=True)


#Producto
class Producto(models.Model):
    pkProducto = models.AutoField(primary_key=True)
    fkSubCategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=300, default = "null")
    descripcion = models.CharField(max_length=1024)
    iva = models.FloatField( default=0, validators=[MinValueValidator(0.1), MaxValueValidator(0.99)],)
    precio = models.IntegerField()
    rutaImagen = models.ImageField(upload_to = '../media/productosImagenes')###############
    #toma todos los productos dados
    #retorna lista de productos con el precio cambiado, si tiene al menos un descuento activo
    #si tienen mas de uno toma el mayor
    #sino retorna el mismo objeto con solamente el iva aplicado
    def productosConDescuento(self,subCategoria,hoy,*args, **kwargs):
        from ventas.models import DescuentoProducto, DescuentoCategoria, DescuentoSubCategoria
        #variables para guardar mayor
        maxdp = 0.0
        maxdc = 0.0
        maxdsc = 0.0
        #descuento activos para la fecha presente
        descuentosProductos = DescuentoProducto.objects.filter(fechaFin__gte=hoy).filter(fechaInicio__lte=hoy)
        descuentosCategorias = DescuentoCategoria.objects.filter(fechaFin__gte=hoy).filter(fechaInicio__lte=hoy)
        descuentosSubCategorias = DescuentoSubCategoria.objects.filter(fechaFin__gte=hoy).filter(fechaInicio__lte=hoy)
        #productos con descuento de producto
        for dp in descuentosProductos:
            productosConDp = Producto.objects.filter(fkSubCategoria=subCategoria).filter(pkProducto = dp.fkProducto.pkProducto)
        #productos con descuento de subcategoria
        for dsc in descuentosSubCategorias:
            #si el descuento en que estoy es de mi subcategoria
            if (dsc.fkSubCategoria.pkSubCategoria != subCategoria):
                continue
            else:
                #obtengo los productos de mi subcategoria
                productosConDc = Producto.objects.filter(fkSubCategoria=subCategoria)
        #productos con descuento de categoria
        for dc in descuentosCategorias:
            #si el descuento en que estoy es de mi categoria
            if (dc.fkCategoria != SubCategoria.objects.get(pkSubCategoria = subCategoria).fkCategoria):
                continue
            else:
                #obtengo los productos de mi categoria
                productosConDc = Producto.objects.filter(fkSubCategoria=subCategoria)
                

            
        productos = Producto.objects.filter(fkSubCategoria=subCategoria)
        result = []
        #iva
        for p in productos:
            p.precio = p.precio - (p.precio * p.iva)
            result.append(p)
        return result
            

                
                





#Proveedor
class Proveedor(models.Model):
    pknit = models.CharField(primary_key=True, max_length=16)
    direccion = models.CharField(max_length=128)
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{7,10}$', message="El telefono debe tener formato: '+7777777'. Up to 10 digits allowed.")
    telefono = models.CharField(validators=[telefono_regex], max_length=12, blank=True)

#Bodega
class Bodega(models.Model):
    CIUDAD = {
        ('BOG','Bogotá'),
        ('MED','Medellín'),
        ('CALI','Cali'),
        ('B/Q','Barranquilla'),
        ('CART','Cartagena'),
        ('CUC','Cucuta'),
        ('SOL','Soledad'),
        ('IBG','Ibague'),
        ('BCM','Bucaramanga'),
        ('SOAC','Soacha'),
    }
    pkBodega = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=128)
    ciudad = models.CharField(max_length=4, choices = CIUDAD, default='CALI')


#DetallesProducto
class DetallesProducto(models.Model):            
    COLOR = {
        ('negro',' Negro'),
        ('blanco','Blanco'),
        ('amarillo','Amarillo'),
        ('azul','Azul'),
        ('rojo','Rojo'),
        ('verde','Verde'),
        ('morado','Morado'),
        ('naranja','Naranja'),
        ('rosado','Rosado'),
        ('gris','Gris'),
        ('marron','Marrón'),
        ('beige','Beige'),
        ('otros','Otro'),
    }
    fkProducto =  models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=32)
    nit = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    color = models.CharField(max_length=64, choices=COLOR)
    fkBodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
