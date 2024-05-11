from django import forms
from .models import LoginInfo

class Login_Info(forms.ModelForm):
    # score = forms.FloatField()
    firstName = forms.CharField(max_length=255)
    lastName = forms.CharField(max_length=255)
    pais = forms.CharField(max_length=50)
    ciudad = forms.CharField(max_length=50)
    email = forms.CharField(max_length=255)
    numero = forms.CharField(max_length=50)

    class Meta:
        model = LoginInfo
        fields = [
            'firstName',
            'lastName',
            'pais',
            'ciudad',
            'email',
            'numero',
        ]

    def clean_firstName(self):
        return self.cleaned_data.get('firstName')
    
    def clean_lastName(self):
        return self.cleaned_data.get('lastName')
    
    def clean_pais(self):
        return self.cleaned_data.get('pais')
    
    def clean_ciudad(self):
        return self.cleaned_data.get('ciudad')
    
    def clean_email(self):
        return self.cleaned_data.get('email')
    
    def clean_numero(self):
        return self.cleaned_data.get('numero')


class otpForm(forms.Form):
    otpNumber = forms.IntegerField()

    class Meta:
        fields = [
            'otpNumber',
        ]

    def clean_otpNumber(self):
        return self.cleaned_data.get('otpNumber')