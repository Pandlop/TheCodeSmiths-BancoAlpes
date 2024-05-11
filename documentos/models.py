from django.db import models
import hashlib
# Create your models here.

"""
class DocumentoFirma(models.Model):
    firma = models.TextField()
    archivo = models.FileField()

    def __str__(self):
        return '%s %s'.format(self.tamanio,self.firma)
"""    


class DocumentoCarga(models.Model):
    score = models.FloatField(null=True)
    archivo = models.FileField(null=False,default=None)
    estado = models.IntegerField(null=False, default=1)
    tipo = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{}'.format(self.archivo)


    
