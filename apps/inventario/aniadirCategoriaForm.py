from django import forms

from inventario.models import Categoria

class AniadirCategoriaForm(forms.Form):
    class Meta:
        model = Categoria

        fields = [
            'nombre',
        ]

        labels = {
            'nombre': 'Nombre',
        }

        widgets = {
            'nombre': forms.TextInput(attrs = {'class': 'form-control'}),
        }