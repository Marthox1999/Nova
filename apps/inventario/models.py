from django.db import models

# Create your models here.

#Categoria
class Categoria(models.Model):
    pkCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=256)

    def __str__(self):
        return self.nombreCategoria

#Subcategoria
class SubCategoria(models.Model):
    pkSubCategoria = models.AutoField(primary_key=True)
    fkCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombreSubCategoria = models.CharField(max_length=256)

#Producto
class Producto(models.Model):
    pkProducto = models.AutoField(primary_key=True)
    fkSubCategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=1024)
    iva = models.FloatField()
    precio = models.IntegerField()
    rutaImagen = models.ImageField(upload_to = '../productosImagenes', default = '..productosImagenes/no-img.jpg')###############

#Proveedor
class Proveedor(models.Model):
    pknit = models.CharField(primary_key=True, max_length=16)
    direccion = models.CharField(max_length=128)
    telefono = models.CharField(max_length=10)

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
    fkProducto =  models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=32)
    nit = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)#quizas una lista de colores en vez de escribirlo?
    fkBodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
