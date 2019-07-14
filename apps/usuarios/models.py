from django.db import models
import hashlib

class Cliente(models.Model):
    TIPO_DOC = {
        ('PAS','Pasaporte'),
        ('CC','Cedula de Ciudadania'),
        ('TI','Tarjeta de Identidad'),
    }
    pkCliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32)
    clave = models.CharField(max_length=32, editable=True)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=32)
    telefono = models.CharField(max_length=10)
    tipoDocumento = models.CharField(max_length=3, choices = TIPO_DOC)
    numeroDocumento = models.IntegerField()

    #super().save(*args, **kwargs) para guardar en esta tabla   
    def save(self, *args, **kwargs):       
        self.clave = hashlib.md5(self.clave.encode('utf-8')).hexdigest()
        super(Cliente, self).save(*args, **kwargs)

class AdministradorDuenio (models.Model):
    TIPO = {
        ('ADMIN','Administrador'),
        ('CEO','Duenio'),
    }
    pkAdministradorDuenio = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=8)
    clave = models.CharField(max_length=16, editable=False)
    tipo = models.CharField(max_length=5, choices=TIPO) 

    #super().save(*args, **kwargs) para guardar en esta tabla
    def save(self, *args, **kwargs):       
        self.clave = hashlib.md5(self.clave.encode('utf-8')).hexdigest()
        super(AdministradorDuenio, self).save(*args, **kwargs)
