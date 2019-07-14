from django import forms

from usuarios.models import Cliente

class IngresarClienteForm(forms.Form):

    class Meta:
        model = Cliente

        fields = [
            'nombre',
            'clave',
        ]

        labels = {
            'nombre': 'nombre',
            'clave': 'clave',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'clave': forms.TextInput(attrs={'class':'form-control'}),
        }
