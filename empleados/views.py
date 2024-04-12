from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Empleado
from documentos.models import DocumentoCarga

# Create your views here.


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
            documentos = DocumentoCarga.objects.all()
            return render(request, 'vistaEmpleadoDocs.html', {'documentos': documentos})
    else:
        return redirect('login_view')

    

def logout_view(request):
    logout(request)
    return redirect('login_view')


def aprobar(request, id):
    """
    -1 -> No revisado
    0 -> Rechazado
    1 -> En revisión
    2 -> Aprobado
    """
    documento = DocumentoCarga.objects.get(pk=id)
    documento.estado = 2
    documento.save()
    return redirect('vistaDocs')


def rechazar(request, id):
    """
    -1 -> No revisado
    0 -> Rechazado
    1 -> En revisión
    2 -> Aprobado
    """
    documento = DocumentoCarga.objects.get(pk=id)
    documento.estado = 0
    documento.save()
    return redirect('vistaDocs')