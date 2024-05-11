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
    # hash_archivo = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.archivo)

    # def save(self, *args, **kwargs):
    #     # Actualizar el hash del archivo cada vez que se guarda el modelo
    #     if self.archivo:
    #         self.hash_archivo = self.generate_hash()
    #     super(DocumentoCarga, self).save(*args, **kwargs)
        

    # def generate_hash(self):
    #     """Genera un hash SHA-256 del contenido del archivo."""
    #     sha256 = hashlib.sha256()
    #     with self.archivo.open(mode='rb') as file:  # Abrir el archivo en modo binario
    #         if self.archivo.multiple_chunks():
    #             for chunk in file.chunks():  # Usa 'file' en lugar de 'self.archivo.file'
    #                 sha256.update(chunk)
    #         else:
    #             data = file.read()  # Usa 'file' en lugar de 'self.archivo'
    #             sha256.update(data)
    #     return sha256.hexdigest()

    
