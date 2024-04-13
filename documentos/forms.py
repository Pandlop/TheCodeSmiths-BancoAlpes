from django import forms
from .models import DocumentoCarga

class ArchivoForm(forms.ModelForm):
    # score = forms.FloatField()
    ccFrontal = forms.FileField()
    ccTrasera = forms.FileField()
    desprendiblePago1 = forms.FileField()
    desprendiblePago2 = forms.FileField()

    class Meta:
        model = DocumentoCarga
        fields = [
            'ccFrontal',
            'ccTrasera',
            'desprendiblePago1',
            'desprendiblePago2'
        ]