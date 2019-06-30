from django.db import models

# Create your models here.
class Product (models.Model):
    nombre = models.CharField(max_length = 20)
    precio = models.CharField(max_length= 10)
