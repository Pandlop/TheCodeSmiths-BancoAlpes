from django.shortcuts import render, redirect
from django.template import loader
from .logic import logic_documentosCarga as ldc
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def documentosCarga_template(request):
    template = loader.get_template('documentosCarga.html')
    return HttpResponse(template.render())
    
@csrf_exempt
def documentosCarga_view(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id:
            documentoCarga_dto = ldc.get_documentoCarga(id)
            documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
            return HttpResponse(documentoCarga, 'application/json')
        else:
            documentosCarga_dto = ldc.get_documentosCarga()
            documentosCarga = serializers.serialize('json', documentosCarga_dto )
            contexto ={'documentosCarga': documentosCarga}
            render(request, 'documentosCarga.html',contexto)
        
    if request.method == 'POST':
        documentoCarga_dto = ldc.create_documentoCarga(json.loads(request.body))
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')
    

@csrf_exempt
def documentoCarga_view(request, doc_pk):
    template = loader.get_template('documentosCarga.html')
    if request.method == 'GET':
        documentoCarga_dto = ldc.get_documentoCarga(doc_pk)
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')
        
    if request.method == 'PUT':
        documentoCarga_dto = ldc.update_documentoCarga(doc_pk, json.loads(request.body))
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')