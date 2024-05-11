from django.db import models

# Create your models here.

class LoginInfo(models.Model):
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    pais = models.CharField(max_length=50, null=False)
    ciudad = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=255, null=False)
    numero = models.IntegerField(null=False)
    role = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{}'.format(self.archivo)
    

class userinfo(models.Model):
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    pais = models.CharField(max_length=50, null=False)
    ciudad = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=255, null=False, primary_key=True)
    numero = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "usuarios",
        # db_table = 'bancoAlpes_userinfo'

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}'.format(self.firstName, self.lastName, self.pais, self.ciudad, self.email, self.numero, self.role)