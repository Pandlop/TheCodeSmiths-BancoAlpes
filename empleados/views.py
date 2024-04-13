from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Empleado
from documentos.models import DocumentoCarga
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('vistaDocs')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})
    else:

        if request.user.is_authenticated:
            return redirect('vistaDocs')
        else:
            return render(request, 'login.html')
        
@csrf_exempt
def vistaDocs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # archivo = request.FILES['archivo']
            # score = request.POST.get('score')
            # estado = request.POST.get('estado')
            # documento = DocumentoCarga(archivo=archivo, score=score, estado=estado)
            # documento.save()
            return render(request, 'vistaEmpleadoDocs.html')
        else:
            documentos = DocumentoCarga.objects.filter(estado=1)
            return render(request, 'vistaEmpleadoDocs.html', {'documentos': documentos})
    else:
        return redirect('login_view')

    
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login_view')

@csrf_exempt
def aprobar(request, id):
    """
    0 -> Rechazado
    1 -> En revisión
    2 -> Aprobado
    """
    documento = DocumentoCarga.objects.get(pk=id)
    documento.estado = 2
    documento.save()
    return redirect('vistaDocs')

@csrf_exempt
def rechazar(request, id):
    """
    0 -> Rechazado
    1 -> En revisión
    2 -> Aprobado
    """
    documento = DocumentoCarga.objects.get(pk=id)
    documento.estado = 0
    documento.save()
    return redirect('vistaDocs')