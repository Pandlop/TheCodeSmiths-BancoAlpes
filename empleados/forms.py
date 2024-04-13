from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField()


    class Meta:
        model = DocumentoCarga
        fields = [
            'username',
            'password'
        ]