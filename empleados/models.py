from django.db import models

# Create your models here.

class Empleado(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, unique=True, null=True, default=None)
    email = models.EmailField(max_length=254, null=False, primary_key=True, default=None)
    password = models.CharField(max_length=50, null=True, default=None)
    role = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "empleados",
        # db_table = 'bancoAlpes_userinfo'

    def __str__(self):
        return '{}, {}'.format(self.email, self.role)