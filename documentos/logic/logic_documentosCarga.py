from ..models import DocumentoCarga

def get_documentosCarga():
    documentosCarga = DocumentoCarga.objects.all()
    return documentosCarga

def get_documentoCarga(doc_pk):
    documentoCarga = DocumentoCarga.objects.get(pk=doc_pk)
    return documentoCarga

def create_documentoCarga(doc):
    documentoCarga = DocumentoCarga(archivo=doc["archivo"])
    documentoCarga.save()
    return documentoCarga

def update_documentoCarga(doc_pk, new_doc):
    documentoCarga = get_documentoCarga(doc_pk)
    documentoCarga.archivo = new_doc.archivo
    documentoCarga.score = new_doc.score
    documentoCarga.save()
    return documentoCarga

def delete_documentoCarga(doc_pk):
    documentoCarga = get_documentoCarga(doc_pk)
    documentoCarga.delete()
    return None
