from django.db import models

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

    def __str__(self):
        return '{} {}'.format(self.score,self.archivo)