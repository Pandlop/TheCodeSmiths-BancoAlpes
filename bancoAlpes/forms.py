from django import forms
from .models import LoginInfo

class Login_Info(forms.ModelForm):
    # score = forms.FloatField()
    firstName = forms.CharField(max_length=255)
    lastName = forms.CharField(max_length=255)
    pais = forms.CharField(max_length=50)
    ciudad = forms.CharField(max_length=50)
    email = forms.CharField(max_length=255)

    class Meta:
        model = LoginInfo
        fields = [
            'firstName',
            'lastName',
            'pais',
            'ciudad',
            'email',
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
