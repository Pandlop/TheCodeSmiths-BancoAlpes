from django.db import models

# Create your models here.

class Solicitud(models.Model):
    fecha_solicitud = models.CharField(null=False, max_length=50)
    anio_solicitud = models.IntegerField(null = False)
    estado =  models.IntegerField(null=False,default=0) #0 en proceso, 1 fallido, 2 aprobado
    
    def __str__(self):
        return '{} {} {}'.format(self.fecha_solicitud, self.anio_solicitud, self.estado)