from django.shortcuts import render

from .forms import ArchivoForm
from .models import DocumentoCarga
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .logic import logic_documentosCarga as ldc
from django.core import serializers
from django.http import HttpResponse
import json
from google.cloud import  vision
from django.views.decorators.csrf import csrf_exempt

import threading
import io
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import os
import base64
from django.contrib.auth.decorators import login_required

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import json
import hashlib



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "documentos/keys/bancoalpes-417404-9b703b711492.json"


@csrf_exempt
def file_list(request):
    files = DocumentoCarga.objects.all()
    return render(request, 'documentosCarga_list.html', {'files': files})


@csrf_exempt
def list_docs(request):
    
    docsExitosos = False

    if request.method == 'POST':

        integ = revisarIntegridad(request) == 1
        print("Integridad = " , integ)
        if(integ == 1):
            
            


            form = ArchivoForm(request.POST, request.FILES)
            if form.is_valid():
                

                ccFrontal = request.FILES.getlist('ccFrontal_file')
                ccTrasera = request.FILES.getlist('ccTrasera_file')
                desprendiblePago1 = request.FILES.getlist('desprendiblePago1_file')
                desprendiblePago2 = request.FILES.getlist('desprendiblePago2_file')

                archivos_listas = [
                    request.FILES.getlist('ccFrontal_file'),
                    request.FILES.getlist('ccTrasera_file'),
                    request.FILES.getlist('desprendiblePago1_file'),
                    request.FILES.getlist('desprendiblePago2_file'),
                ]


                # Verificar que todos los archivos sean PNG
                todos_png = all(os.path.splitext(f.name)[1].lower() == '.png' for lista in archivos_listas for f in lista)
                
                if not todos_png:
                    # messages.error(request, 'Todos los archivos deben ser PNG.')
                    return render(request, 'documentosCarga.html', {
                        'documentosSubidos': DocumentoCarga.objects.all(),
                        'docsExitosos': False,
                        'post': True,
                        'message': 'Error: Todos los archivos deben ser PNG.'
                    })
                
                threads = []
                lock = threading.Lock()


                for f in ccFrontal:
                    
                    instanciaCcFrontal = DocumentoCarga(archivo=f)
                    instanciaCcFrontal.tipo = 'ccFrontal'
                    # asignarScoreG(instanciaCcFrontal, 'ccFrontal')
                    # if(instanciaCcFrontal.score <= 0.6):
                    #     instanciaCcFrontal.estado = 0 
                    # instanciaCcFrontal.save()
                    threadccFrontal = threading.Thread(target=asignarScoreG, args=(instanciaCcFrontal, 'ccFrontal', lock))
                    
                for f in ccTrasera:
                    instanciaCcTrasera = DocumentoCarga(archivo=f)
                    instanciaCcTrasera.tipo = 'ccTrasera'
                    # asignarScoreG(instanciaCcTrasera, 'ccTrasera')
                    # if(instanciaCcTrasera.score <= 0.6):
                    #     instanciaCcTrasera.estado = 0 
                    # instanciaCcTrasera.save()
                    threadccTrasera = threading.Thread(target=asignarScoreG, args=(instanciaCcTrasera, 'ccTrasera', lock))

                    
                for f in desprendiblePago1:
                    instanciaDesprendiblePago1 = DocumentoCarga(archivo=f)
                    instanciaDesprendiblePago1.tipo = 'desprendiblePago'
                    # asignarScoreG(instanciaDesprendiblePago1, 'desprendiblePago')
                    # if(instanciaDesprendiblePago1.score <= 0.6):
                    #     instanciaDesprendiblePago1.estado = 0 
                    # instanciaDesprendiblePago1.save()
                    threaddesprendiblePago1 = threading.Thread(target=asignarScoreG, args=(instanciaDesprendiblePago1, 'desprendiblePago', lock))


                for f in desprendiblePago2:
                    instanciaDesprendiblePago2 = DocumentoCarga(archivo=f)
                    instanciaDesprendiblePago2.tipo = 'desprendiblePago'
                    # asignarScoreG(instanciaDesprendiblePago2, 'desprendiblePago')
                    # if(instanciaDesprendiblePago2.score <= 0.6):
                    #     instanciaDesprendiblePago2.estado = 0 
                    # instanciaDesprendiblePago2.save()
                    threaddesprendiblePago2 = threading.Thread(target=asignarScoreG, args=(instanciaDesprendiblePago2, 'desprendiblePago', lock))

                threads.append(threadccFrontal)
                threads.append(threadccTrasera)
                threads.append(threaddesprendiblePago1)
                threads.append(threaddesprendiblePago2)

                print("Creando T1")
                threadccFrontal.start()
                print("Creando T2")
                threadccTrasera.start()
                print("Creando T3")
                threaddesprendiblePago1.start()
                print("Creando T4")
                threaddesprendiblePago2.start()

                i=0
                for t in threads:
                    print("Esperando a T", i+1)
                    t.join(timeout=2)
                    print("T", i+1, "terminó")
                    i+=1

                if(instanciaCcFrontal.score < 0.6):
                    instanciaCcFrontal.estado = 0 
                instanciaCcFrontal.save()

                if(instanciaCcTrasera.score < 0.6):
                    instanciaCcTrasera.estado = 0
                instanciaCcTrasera.save()

                if(instanciaDesprendiblePago1.score < 0.6):
                    instanciaDesprendiblePago1.estado = 0
                instanciaDesprendiblePago1.save()

                if(instanciaDesprendiblePago2.score < 0.6):
                    instanciaDesprendiblePago2.estado = 0
                instanciaDesprendiblePago2.save()


                documentos_subidos = DocumentoCarga.objects.all()
                context = {
                    'documentosSubidos': documentos_subidos,
                    'docsExitosos': True,
                    'post': True,
                    'message': 'Los archivos se han subido con éxito.'
                }
                return render(request, 'documentosCarga.html', context, 'application/json')
            
            else:
                documentosSubidos = DocumentoCarga.objects.all()
                docsExitosos = False
                
                # El formulario no es válido, extraer el primer error
                primer_error = None

                # Buscar el primer error de un campo específico
                for field in form:
                    if field.errors:
                        primer_error = str(field.errors[0])
                        break

                # Si no hay errores de campo, verificar errores generales del formulario
                if not primer_error:
                    if form.non_field_errors():
                        primer_error = str(form.non_field_errors()[0])

                message = primer_error
                context = {'documentosSubidos': documentosSubidos, "docsExitosos":docsExitosos, "message": message, "post":True}
                
                return render(request, 'documentosCarga.html', context)
        else:
            print("Estoy en el error")

            return HttpResponse('Documento no encontrado', status=412)
    else:
        documentos_subidos = DocumentoCarga.objects.all()
        context = {'documentosSubidos': documentos_subidos, 'docsExitosos': False, 'post': False}
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
        return HttpResponse(request, 'application/json')
    elif request.method=="PUT":
        data = json.loads(request.body)
        new_doc = DocumentoCarga(archivo = data)
        documentoCarga_dto = ldc.update_documentoCarga(docId,new_doc)
        documentoCarga = serializers.serialize('json', [documentoCarga_dto,])
        return HttpResponse(documentoCarga, 'application/json')

@csrf_exempt
# Funcion para la pagina de inicio de los documentos
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')

@csrf_exempt
# Funcion para asignar un score a un documento con el api de google
def asignarScoreG(instancia, tipoDoc, lock):

    if tipoDoc == 'desprendiblePago':

        with lock:

            text = detect_text(instancia.archivo.open())

            palabraClave = {
                    'nombre': 5, 'cédula': 5, 'fecha': 2, 'valor': 5, 'concepto': 2, 'nómina': 2,
                    'periodo': 2, 'empresa': 2, 'codigo': 1, 'nit': 5, 'direccion': 1,
                    'telefono': 1, 'ciudad': 1, 'correo': 1, 'pago': 1, 'total': 3,
                    'neto': 3, 'deducciones': 1, 'caja': 1, 'compensacion': 1, 'identificación': 5, 'documento': 5,
                    'documento de identidad': 5, 'salario': 5, 'ingresos': 5, 'deducciones': 1, 'ingreso': 5, 'factura': -10,
                    'cliente': -10, 'servicio': -10, 'producto': -10, 'vendedor': -10
            }

            total_palabras_clave = len(palabraClave)
            score = 0

            for palabra, peso in palabraClave.items():
                if (palabra in text or palabra.upper() in text or palabra.capitalize() in text):
                        score += peso

            if score / total_palabras_clave >= 1:
                instancia.score = 1
            elif score / total_palabras_clave <= 0:
                instancia.score = 0
            else:
                instancia.score = score / total_palabras_clave

            instancia.save()
    
    elif tipoDoc == "ccFrontal":

        print("Voy a hacer la pericion a la cedula frontal")

        with lock:
        

            text = detect_text(instancia.archivo.open())

            print("Peticion 1 hecha, voy con la 2")

            scoreFace = detect_faces(instancia.archivo.open())

            print("Peticion 2 hecha")
            
            print ("Fuera del lock")

            palabraClave = {
                    'cédula de ciudadanía': 10, 'república de colombia': 10, 'apellidos': 5,
                    'nombres': 5, 'nacionalidad': 5, 'estatura': 5, 'sexo': 5, 'fecha de nacimiento': 5,
                    'lugar de nacimiento': 5, 'fecha y lugar de expedición': 5, 'fecha de expiración': 5, 'firma': 5, 'nuip': 10,
            }

            total_palabras_clave = sum(palabraClave.values())
            score = 0

            for palabra, peso in palabraClave.items():
                if (palabra in text or palabra.upper() in text or palabra.capitalize() in text):
                    score += peso

            totalScore = ((score / total_palabras_clave) + scoreFace) / 2
            # totalScore = ((score / total_palabras_clave) + 0) / 2

            if totalScore >= 1:
                instancia.score = 1
            elif totalScore <= 0:
                instancia.score = 0
            else:
                instancia.score = totalScore

            instancia.save()

    elif tipoDoc == "ccTrasera":

        with lock:

            text = detect_text(instancia.archivo.open())

            palabraClave = {
                    '.CO': 10, 'REGISTRADOR NACIONAL': 10, 'ICCOLO': 10,
            }

            total_palabras_clave = sum(palabraClave.values())
            score = 0

            for palabra, peso in palabraClave.items():
                if (palabra in text or palabra.upper() in text or palabra.capitalize() in text):
                    score += peso

            if score / total_palabras_clave >= 1:
                instancia.score = 1
            elif score / total_palabras_clave <= 0:
                instancia.score = 0
            else:
                instancia.score = score / total_palabras_clave

            instancia.save() 


@csrf_exempt
def detect_text(file): 
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    content = file.read()
    
    if not content:
        raise Exception("File is empty")

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    texts = response.text_annotations
    if texts:
        text = texts[0].description
    else:
        text = ""
    
    file.seek(0)
    return text


@csrf_exempt
def detect_faces(file):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()
    content = file.read()
    
    if not content:
        raise Exception("File is empty")

    image = vision.Image(content=content)
    response = client.face_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    faces = response.face_annotations
    file.seek(0)

    if len(faces) != 1:
        return -1
    return faces[0].detection_confidence

@csrf_exempt
def revisarIntegridad(request):
    
    verificados = 0;

    if request.method == 'POST':
        response_data = {}
        for key in request.FILES:
            if key.endswith('_file'):
                file = request.FILES[key]
                hash_key = key.replace('_file', '_hash')
                hashFile = request.POST[hash_key]

                # Verificar el hash
                hash_obj = hashlib.sha256()
                # Leer el contenido del archivo en fragmentos para no sobrecargar la memoria
                for chunk in file.chunks():
                    hash_obj.update(chunk)
                hash_obj.hexdigest()

                print("Hash del archivo: ", hash_obj.hexdigest())
                print("Hash del archivo en el request: ", hashFile)


                if  hash_obj.hexdigest() != hashFile:
                    return -1
                    break;
                else:
                    verificados +=1
                        
        if(verificados==4):
            return 1     
       
    

