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

    def clean_ccFrontal(self):
        return self.validate_file_size(self.cleaned_data.get('ccFrontal'))

    def clean_ccTrasera(self):
        return self.validate_file_size(self.cleaned_data.get('ccTrasera'))

    def clean_desprendiblePago1(self):
        return self.validate_file_size(self.cleaned_data.get('desprendiblePago1'))

    def clean_desprendiblePago2(self):
        return self.validate_file_size(self.cleaned_data.get('desprendiblePago2'))

    def validate_file_size(self, archivo):
        if archivo:
            # 10 MB = 10 * 1024 * 1024 Bytes
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("El tamaño del archivo no puede superar los 10 MB.")
        return archivo