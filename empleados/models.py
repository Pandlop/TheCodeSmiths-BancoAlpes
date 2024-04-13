from django.db import models

# Create your models here.

class Empleado(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, unique=True, null=False, default=None)
    email = models.EmailField(max_length=254, null=True)
    password = models.CharField(max_length=50, null=False, default=None)
    tipo = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)