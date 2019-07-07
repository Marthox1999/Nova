from django.contrib import admin

# Register your models here.

from .models import Cliente, AdministradorDuenio

admin.site.register(Cliente)
admin.site.register(AdministradorDuenio)