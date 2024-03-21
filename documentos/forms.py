from django import forms
from .models import DocumentoCarga

class ArchivoForm(forms.ModelForm):
    # score = forms.FloatField()
    archivo = forms.FileField()
    class Meta:
        model = DocumentoCarga
        fields = [
            'archivo'
        ]