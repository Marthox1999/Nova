from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

#Categoria
class Categoria(models.Model):
    pkCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=256, unique=True)
    rutaImagen = models.ImageField(upload_to = '../media/categoriasImagenes')###############

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
    iva = models.FloatField()
    precio = models.IntegerField()
    rutaImagen = models.ImageField(upload_to = '../media/productosImagenes')###############

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
        ('Negro',' Negro'),
        ('Blanco','Blanco'),
        ('Amarillo','Amarillo'),
        ('Azul','Azul'),
        ('Rojo','Rojo'),
        ('Verde','Verde'),
        ('Morado','Morado'),
        ('Naranja','Naranja'),
        ('Rosado','Rosado'),
        ('Gris','Gris'),
        ('Marron','Marrón'),
        ('Beige','Beige'),
        ('Otros','Otro'),
    }
    pkDetallesP = models.AutoField(primary_key=True)
    fkProducto =  models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=32)
    nit = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    color = models.CharField(max_length=64, choices=COLOR)
    fkBodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
