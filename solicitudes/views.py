from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Solicitud
import json
from django.http import JsonResponse
from .logic import logic_solicitudes as ls

# Create your views here.
@csrf_exempt
def indexSolicitudes(request):

    if request.method == "GET":

        solicitudes = Solicitud.objects.all()
        totalSolicitudes = solicitudes.count()

        

        solicitudes_aprobadas = Solicitud.objects.filter(estado=2)  
        totalAprobadas = solicitudes_aprobadas.count()

        solicitudes_anio_ant = Solicitud.objects.filter(anio_solicitud=2023)  
        solicitudes_anio_sig = Solicitud.objects.filter(anio_solicitud=2024) 
        
        totalAumento = solicitudes_anio_sig.count() - solicitudes_anio_ant.count()
        
        context = {
            'solicitudes': solicitudes,
            'totalSolicitudes': totalSolicitudes,
            'totalAprobadas': totalAprobadas,
            'totalAumento': totalAumento
        }
        return render(request, 'indexSolicitudes.html', context)
    else:
        data = json.loads(request.body)
        print(data)
        new_sol = Solicitud(fecha_solicitud=data["fecha_solicitud"],anio_solicitud=data["anio_solicitud"],estado=data["estado"])
        sol_dto = ls.create_solicitud(new_sol)
        return render(request, 'indexSolicitudes.html')
