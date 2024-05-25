from django import forms
from .models import DocumentoCarga

class ArchivoForm(forms.ModelForm):
    # score = forms.FloatField()
    ccFrontal_file = forms.FileField()
    ccTrasera_file = forms.FileField()
    desprendiblePago1_file = forms.FileField()
    desprendiblePago2_file = forms.FileField()

    class Meta:
        model = DocumentoCarga
        fields = [
            'ccFrontal_file',
            'ccTrasera_file',
            'desprendiblePago1_file',
            'desprendiblePago2_file'
        ]

    def clean_ccFrontal(self):
        return self.validate_file_size(self.cleaned_data.get('ccFrontal_file'))

    def clean_ccTrasera(self):
        return self.validate_file_size(self.cleaned_data.get('ccTrasera_file'))

    def clean_desprendiblePago1(self):
        return self.validate_file_size(self.cleaned_data.get('desprendiblePago1_file'))

    def clean_desprendiblePago2(self):
        return self.validate_file_size(self.cleaned_data.get('desprendiblePago2_file'))

    def validate_file_size(self, archivo):
        if archivo:
            # 10 MB = 10 * 1024 * 1024 Bytes
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("El tamaño del archivo no puede superar los 10 MB.")
        return archivo