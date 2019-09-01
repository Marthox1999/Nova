from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from inventario.models import Producto, Categoria, SubCategoria
from usuarios.models import Cliente

#DescuentoProducto
class DescuentoProducto(models.Model):
    pkDescuentoProducto = models.AutoField(primary_key=True)
    fkProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fechaInicio = models.DateField(default=timezone.now)
    fechaFin = models.DateField() 
    porcentajeDescuento = models.FloatField(
    validators=[MinValueValidator(0.1), MaxValueValidator(0.99)],
)

#DescuentoCategoria
class DescuentoCategoria(models.Model): 
    pkDescuentoCategoria = models.AutoField(primary_key=True)
    fkCategoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    fechaInicio = models.DateField(default=timezone.now)
    fechaFin = models.DateField()
    porcentajeDescuento = models.FloatField(
    validators=[MinValueValidator(0.1), MaxValueValidator(0.99)],
)


#DescuentoSubCategoria
class DescuentoSubCategoria(models.Model):
    pkDescuentoSubCategoria = models.AutoField(primary_key=True)
    fkSubCategoria = models.ForeignKey(SubCategoria,on_delete=models.CASCADE)
    fechaInicio = models.DateField(default=timezone.now)
    fechaFin = models.DateField()
    porcentajeDescuento = models.FloatField(
    validators=[MinValueValidator(0), MaxValueValidator(99)],
)

#Factura
class Factura(models.Model):
    pkFactura = models.AutoField(primary_key=True)
    fkCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()

#Detalles Factura
class DetallesFactura(models.Model):
    fkFactura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fkProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.FloatField()

#PagosCredito
class PagosCredito(models.Model):
    ENTIDAD = {
        ('VI','VISA'),
        ('CA','MASTERCARD'),
        ('AX','AMERICANEXPRESS'),
    }
    pkPagosCredito = models.AutoField(primary_key=True)
    fkFactura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    numeroAprobacion = models.CharField(max_length=4) #donde se genera automatico?
    fechaAprobacion = models.DateField()
    entidadAprobacion = models.CharField(max_length=2,choices=ENTIDAD)
    porcentajePago = models.FloatField([MinValueValidator(0), MaxValueValidator(99)],
)
#classDebito
class PagosDebito(models.Model):
    pkPagosDebito = models.AutoField(primary_key=True)
    numeroTarjetaDebito = models.IntegerField()#min_length=16
    fkFactura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    numeroPago = models.CharField(max_length=4) 
    ahorros = models.BooleanField()
    porcentajePago = models.FloatField([MinValueValidator(0), MaxValueValidator(99)],
)