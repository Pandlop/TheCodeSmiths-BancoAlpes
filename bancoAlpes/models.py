from django.db import models

# Create your models here.

class LoginInfo(models.Model):
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    pais = models.CharField(max_length=50, null=False)
    ciudad = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=255, null=False)

    def __str__(self):
        return '{}'.format(self.archivo)
    
