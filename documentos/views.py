# from django.shortcuts import render
# from django.template import loader

# from documentos.forms import ArchivoForm
# from documentos.models import DocumentoCarga
# from .logic import logic_documentosCarga as ldc
# from django.http import HttpResponse
# from django.core import serializers
# import json
# from django.views.decorators.csrf import csrf_exempt


# from django.shortcuts import render, redirect


# @csrf_exempt
# def documentosCarga_template(request):
#     template = loader.get_template('documentosCarga.html')
#     return HttpResponse(template.render())
    
# @csrf_exempt
# def documentosCarga_view(request):
#     if request.method == 'GET':
#         id = request.GET.get('id', None)
#         if id:
#             documentoCarga_dto = ldc.get_documentoCarga(id)
#             documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
#             # return HttpResponse(documentoCarga, 'application/json')
#             return render(request, 'documentosCarga.html', {'documentosCarga': documentoCarga})
#         else:
#             documentosCarga_dto = ldc.get_documentosCarga()
#             documentosCarga = serializers.serialize('json', documentosCarga_dto )
#             # return HttpResponse(documentosCarga, 'application/json')
#             return render(request, 'documentosCarga.html', {'documentosCarga': documentosCarga})
        
#     if request.method == 'POST':
#         documentoCarga_dto = ldc.create_documentoCarga(json.loads(request.body))
#         documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
#         return HttpResponse(documentoCarga, 'application/json')
    


# @csrf_exempt
# def documentoCarga_view(request, doc_pk):
#     template = loader.get_template('documentosCarga.html')
#     if request.method == 'GET':
#         documentoCarga_dto = ldc.get_documentoCarga(doc_pk)
#         documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
#         # return HttpResponse(documentoCarga, 'application/json')
#         return render(request, 'documentosCarga.html', {'documentosCarga': documentoCarga})
        
#     if request.method == 'PUT':
#         documentoCarga_dto = ldc.update_documentoCarga(doc_pk, json.loads(request.body))
#         documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
#         return HttpResponse(documentoCarga, 'application/json')
    

# def cargar_archivos(request):
#     if request.method == 'POST':
#         form = ArchivoForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Procesar cada archivo subido
#             for f in request.FILES.getlist('archivos'):
#                 # Aquí asumimos que tu modelo Archivo tiene un campo 'archivo'
#                 # y opcionalmente, otro campo como 'score' que deberías ajustar según tu modelo
#                 instancia = DocumentoCarga(archivo=f)
#                 instancia.save()
#             return redirect('la_url_después_de_cargar')  # Redirige para evitar el reenvío del formulario
#     else:
#         form = ArchivoForm()

#     # Asume que tienes una lista de objetos Archivo para pasar a tu template
#     lista_documentosCargados = DocumentoCarga.objects.all()
#     return render(request, 'tu_template.html', {'lista_documentosCargados': lista_documentosCargados, 'form': form})






from django.shortcuts import render
from .forms import ArchivoForm
from .models import DocumentoCarga
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .logic import logic_documentosCarga as ldc
from django.core import serializers
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

def file_list(request):
    files = DocumentoCarga.objects.all()
    return render(request, 'documentosCarga_list.html', {'files': files})


def list_docs(request):
    

    docsExitosos = False

    
    
    if request.method == 'POST':

        form = ArchivoForm(request.POST, request.FILES)

        if form.is_valid():

            ccFrontal = request.FILES.getlist('ccFrontal')
            ccTrasera = request.FILES.getlist('ccTrasera')
            desprendiblePago1 = request.FILES.getlist('desprendiblePago1')
            desprendiblePago2 = request.FILES.getlist('desprendiblePago2')

            for f in ccFrontal:
                instancia = DocumentoCarga(archivo=f)
                instancia.save()
            for f in ccTrasera:
                instancia = DocumentoCarga(archivo=f)
                instancia.save()
            for f in desprendiblePago1:
                instancia = DocumentoCarga(archivo=f)
                instancia.save()
            for f in desprendiblePago2:
                instancia = DocumentoCarga(archivo=f)
                instancia.save()

            messages.success(request, 'Archivo subido correctamente')

            docsExitosos = True
            
            return HttpResponseRedirect(reverse('list_docs'))
        
        else:
            docsExitosos = False
            return render(request, 'docsFallidos.html')
    else:
            documentosSubidos = DocumentoCarga.objects.all()
            context = {'documentosSubidos': documentosSubidos, 'docsExitosos': docsExitosos}
            return render(request, 'documentosCarga.html', context)   
    
        
        
@csrf_exempt
def list_docs_id(request,docId):
    if request.method=="GET":
        documentoCarga_dto = ldc.get_documentoCarga(docId)
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')
        # return render(request, 'documentosCarga.html', {'documentosCarga': documentoCarga})
    elif request.method=="DELETE":
        documentoCarga_dto = ldc.delete_documentoCarga(docId)
        return HttpResponse(request)
    elif request.method=="PUT":
        data = json.loads(request.body)
        new_doc = DocumentoCarga(archivo = data)
        documentoCarga_dto = ldc.update_documentoCarga(docId,new_doc)
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')



    

# Funcion para la pagina de inicio de los documentos
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')


def docsFallidos(request):
    return render(request, 'docsFallidos.html')