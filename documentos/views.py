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



# -*- coding: utf-8 -*-


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

import requests
import threading

import os


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
                print("Entré a desprendiblePago1")
                instanciaDesprendiblePago1 = DocumentoCarga(archivo=f)
                print("Instancia desprendiblepago1 creada")

                print("voy a crear el thread de desprendiblePago1")
                threadDesprendiblePago1 = threading.Thread(target=asignarScore, args=(instanciaDesprendiblePago1, 'desprendiblePago'))
                print("Thread de desprendiblePago1 creado")

                # instancia.save()

            for f in desprendiblePago2:
                print("Entré a desprendiblePago2")
                instanciaDesprendiblePago2 = DocumentoCarga(archivo=f)
                print("Instancia desprendiblepago2 creada")

                print("voy a crear el thread de desprendiblePago2")
                threadDesprendiblePago2 = threading.Thread(target=asignarScore, args=(instanciaDesprendiblePago2, 'desprendiblePago'))
                print("Thread de desprendiblePago2 creado")

                # instancia.save()

            print("Voy a iniciar los threads")
            threadDesprendiblePago1.start()
            threadDesprendiblePago2.start()
            print("Threads iniciados")

            print("Voy a esperar a que los threads terminen")
            threadDesprendiblePago1.join()
            threadDesprendiblePago2.join()
            print("Threads terminados")
            

            messages.success(request, 'Archivo subido correctamente')

            docsExitosos = True
            
            return HttpResponseRedirect(reverse('confirmacion'))
        
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


def confirmacion(request):
    return render(request, 'pantallaConfirmacion.html')



# Funcion para asignar un score a un documento
def asignarScore(instancia, tipoDoc):

    urlLink = 'https://api.ocr.space/parse/image'
    apiKey = '79d467c37288957'

    payload = {
        'apikey': '79d467c37288957',
        'language': 'spa',
    }

    if tipoDoc == 'desprendiblePago':

        print("Voy a hacer la petición de OCR desprendible de pago")
        response = requests.post(urlLink, data=payload, files={'file': instancia.archivo})
        print("peticion de OCR desprendible de pago hecha")
        # print(response.content)
        jsonResponse = json.loads(response.content)

        if response.status_code == 200:
        #     print("Desprendible de pago 1:")
        #     score = asignarScore(response, 'desprendiblePago')
        #     print("")
        #     instancia.score = score
        # else:
        #     print('Error en la petición de OCR ccFrontal')


            palabraClave = {
                'nombre': 5, 'cédula': 5, 'fecha': 2, 'valor': 5, 'concepto': 2, 'nómina': 2,
                'periodo': 2, 'empresa': 2, 'codigo': 1, 'nit': 5, 'direccion': 1,
                'telefono': 1, 'ciudad': 1, 'correo': 1, 'pago': 1, 'total': 3,
                'neto': 3, 'deducciones': 1, 'caja': 1, 'compensacion': 1, 'identificación': 5, 'documento': 5,
                'documento de identidad': 5, 'salario': 5, 'ingresos': 5, 'deducciones': 1, 'ingreso': 5, 'factura': -10,
                'cliente': -10, 'servicio': -10, 'producto': -10, 'vendedor': -10
            }

            # total_palabras_clave = sum(palabraClave.values())
            total_palabras_clave = len(palabraClave)
            score = 0

            for palabra, peso in palabraClave.items():
                if (palabra in jsonResponse['ParsedResults'][0]['ParsedText'] or
                        palabra.upper() in jsonResponse['ParsedResults'][0]['ParsedText'] or
                        palabra.capitalize() in jsonResponse['ParsedResults'][0]['ParsedText']):
                    score += peso

            # if score / total_palabras_clave >= 1:
            #     return 1
            # elif score / total_palabras_clave <= 0:
            #     return 0
            # else:
            #     return score / total_palabras_clave

            print("Score del desprendible de pago: ", score / total_palabras_clave)
            if score / total_palabras_clave >= 1:
                instancia.score = 1
            elif score / total_palabras_clave <= 0:
                instancia.score = 0
            else:
                instancia.score = score / total_palabras_clave

            print("Score asignado al desprendible de pago: ", instancia.score)
            instancia.save()
            print("Score guardado en la base de datos")
        
        else:
            print('Error en la petición de OCR desprendible de pago')