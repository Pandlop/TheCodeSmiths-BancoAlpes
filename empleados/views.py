from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from bancoAlpes.models import userinfo

from .models import Empleado
from documentos.models import DocumentoCarga
from django.views.decorators.csrf import csrf_exempt

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus, urlencode


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID_EMPLEADOS,
    client_secret=settings.AUTH0_CLIENT_SECRET_EMPLEADOS,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN_EMPLEADOS}/.well-known/openid-configuration",
)

@csrf_exempt
def login_empleado(request):

    if "user_token" in request.session:

        token = request.session["user_token"]
        infoEmpleado = token['userinfo']
        email = infoEmpleado['email']

        empleado = Empleado.objects.filter(email=email).first()
        print(empleado, "empleado desde login_empleado")

        if empleado and empleado.role == 'empleado':
            return redirect('vistaDocs')
        
        cliente = userinfo.objects.filter(email=email).first()

        if cliente and cliente.role == 'cliente':
            return redirect('landingPage')
    
    else:
        
        return oauth.auth0.authorize_redirect(
            request, request.build_absolute_uri(reverse("callback_empleado")),
            connection='Username-Password-Authentication'
        )
    
    render (request, 'landingPage.html')
    


@csrf_exempt
def callback_empleado(request):
    token = oauth.auth0.authorize_access_token(request)

    request.session["user_token"] = token
    print(token, "desde el callback_empleado")

    infoEmpleado = token['userinfo']
    email = infoEmpleado['email']


    empleadoInfo = Empleado(email=email)
    empleadoInfo.role = "empleado"

    print(empleadoInfo, "empleadoInfo desde callback_empleado")

    # ---------------------------- 

    empleadoInfo.save()

    print("ya guardé el empleado")

    usuarios = Empleado.objects.filter(email=email)

    print("Estos son los usuarios guardados", usuarios)
    for usuario in usuarios:
        print(usuario, "usuario")

    # ----------------------------

    print("ya estoy saliendo del callback_empleado")

    return redirect(request.build_absolute_uri(reverse("vistaDocs")))

@csrf_exempt
def logout_empleados(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("login_view")),
                "client_id": settings.AUTH0_CLIENT_ID_EMPLEADOS,
            },
            quote_via=quote_plus,
        ),
    )

@csrf_exempt
def login_view(request):
    if request.method == 'POST':

        if "user_token" in request.session:

            token = request.session["user_token"]
            infoEmpleado = token['userinfo']
            email = infoEmpleado['email']


            empleado = Empleado.objects.filter(email=email).first()

            if empleado and empleado.role == 'empleado':
                return redirect('vistaDocs')
            else:
                return render(request, 'login.html', {'error': 'Usuario no autorizado.'})
            
        else:
            return redirect('login_empleado')
        
    else:
        return render(request, 'login.html')


@csrf_exempt
def vistaDocs(request):

    if request.method == 'GET':

        if "user_token" in request.session:

            token = request.session["user_token"]
            infoEmpleado = token['userinfo']
            email = infoEmpleado['email']


            empleado = Empleado.objects.filter(email=email).first()

            if empleado and empleado.role == 'empleado':
                documentos = DocumentoCarga.objects.filter(estado=1)
                return render(request, 'vistaEmpleadoDocs.html', {'documentos': documentos})
            else:
                return redirect('/landingPage')
            
        else:
            return redirect('login_view')
        
    else:
        return redirect('login_empleado')
    

def verificarLogin(request):
    
    if "user_token" in request.session:
        return redirect('landingPage')
    else:
        return redirect('login_empleado')

    
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