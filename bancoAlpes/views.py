import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
import requests

from empleados.models import Empleado

from .models import userinfo
from .forms import Login_Info, otpForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from urllib.parse import quote_plus, urlencode
from django.views.decorators.csrf import csrf_exempt
from time import sleep


from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from django.core.mail import send_mail
from django.conf import settings

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


#Llave publica
def llavePublica(request):
    try:
        with open("bancoAlpes/llavePublica.pem", "rb") as key_file:
            public_key_pem = key_file.read().decode('utf-8')
        return JsonResponse({"publicKey": public_key_pem})
    except FileNotFoundError:
        return JsonResponse({"error": "Public key not found"}, status=404)


# Cosas de autenticación -------------------------------------------------------


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email update:users",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
@csrf_exempt
def login(request):

    if "user_token" in request.session:

        token = request.session["user_token"]
        return HttpResponse(status=200, content={"token": token})
    else:
        return render(request, "loginPageForm.html")        
        

@csrf_exempt
def callback(request):
    token = oauth.auth0.authorize_access_token(request)

    request.session["user_token"] = token
    print(token, "desde el callback")

    firstName = request.session.get("login_info")["firstName"]
    lastName = request.session.get("login_info")["lastName"]
    pais = request.session.get("login_info")["pais"]
    ciudad = request.session.get("login_info")["ciudad"]
    email = request.session.get("login_info")["email"]
    numero = request.session.get("login_info")["numero"]

    userInfo = userinfo(firstName=firstName, lastName=lastName, pais=pais, ciudad=ciudad, email=email, numero=numero)
    userInfo.role = "cliente"

    print(userInfo, "userInfo desde callback")

    # ---------------------------- 

    # userInfo.save(using='usuarios')
    userInfo.save()
    # userinfo.objects.all().delete()

    print("ya guardé el usuario")

    # usuarios = userinfo.objects.using('usuarios').filter(email=email)
    usuarios = userinfo.objects.filter(email=email)

    print("Estos son los usuarios guardados", usuarios)
    for usuario in usuarios:
        print(usuario, "usuario")

    # ----------------------------

    print("ya estoy saliendo del callback")

    return redirect(request.build_absolute_uri(reverse("landingPage")))

@csrf_exempt
def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("landingPage")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )




@csrf_exempt
def submit_login_info(request):
    request.session.clear()

    first_name = str(request.POST["first_name"])
    last_name = str(request.POST["last_name"])
    country = str(request.POST["country"])
    city = str(request.POST["city"])
    email = str(request.POST["email"])
    phone = str(request.POST["phone"])
    password = str(request.POST["password"])


    request.session["login_info"] = {
        "first_name": first_name,
        "last_name": last_name,
        "country": country,
        "city": city,
        "email": email,
        "phone": phone,
        "password": password
    }

    # Realizar la solicitud POST para obtener el token
    response = requests.post("http://34.49.65.40:80/user/login", json=request.session["login_info"])
    # print(response.text)
    # Verificar si la solicitud fue exitosa
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        # Extraer el token de la respuesta JSON
        request.session["user_token"] = response.json().get("access_token") # Asegúrate de extraer solo el token

        return HttpResponse( request.session["user_token"], status=200)
    else:
        # Manejar el caso de error
        print("sus")
        return HttpResponse("error", status=503)

def loginOTP(request):

    return render(request, 'loginOTP.html')
    
#
def submit_otp(request):

    codigoOTP = request.session.get('otpNumber')
    print(codigoOTP, 'codigoOTP')

    if request.method == 'POST':

        form = otpForm(request.POST)

        if form.is_valid():

            print("es validox")

            otpNumber = request.POST['otpNumber']

            if int(otpNumber) == codigoOTP:
                # return redirect(reverse("landingPage"))
                # return HttpResponse(landingPage, 'application/json')
                return render(request, 'landingPage.html')
            else:
                error = "El código ingresado no es correcto"
                context = {
                    'error': error,
                }
                # return redirect(reverse("loginOTP"))
                # return HttpResponse(loginOTP, 'application/json')
                return render(request, 'loginOTP.html', context)
    else:
        # return redirect(reverse("loginOTP"))
        # return HttpResponse(loginOTP, 'application/json')
        return render(request, 'loginOTP.html')


# Otras funciones ---------------------------------------------------------------

@csrf_exempt
def landingPage(request):

    estaLogueado = "user_token" in request.session;

    if estaLogueado:

        token = request.session["user_token"]
        infoEmpleado = token['userinfo']
        email = infoEmpleado['email']

        empleado = Empleado.objects.filter(email=email).first()

        if empleado and empleado.role == 'empleado':
            return redirect('vistaDocs')
        else:

            context={
                    "session": request.session["user_token"],
                    "pretty": json.dumps(request.session["user_token"], indent=4),
                    "estaLogueado": estaLogueado}
            
            return render(request, 'landingPage.html', context)
    
    else:

        return render(request, 'landingPage.html')

@csrf_exempt
def signupPageForm(request):

    return render(request, 'signupPageForm.html')

@csrf_exempt
def submit_signup_info(request):
    first_name = str(request.POST["first_name"])
    last_name = str(request.POST["last_name"])
    country = str(request.POST["country"])
    city = str(request.POST["city"])
    email = str(request.POST["email"])
    phone = str(request.POST["phone"])
    password = str(request.POST["password"])


    request.session["signup_info"] = {
        "first_name": first_name,
        "last_name": last_name,
        "country": country,
        "city": city,
        "phone": phone,
        "email": email,
        "password": password
    }
    response = requests.post("http://34.49.65.40:80/user/signup", json=request.session["signup_info"])
    return redirect(reverse('loginPageForm'))


@csrf_exempt
def loginPage(request):

    if "user_token" in request.session:

        token = request.session["user_token"]
        return HttpResponse(status=200, content={"token": token})
    else:
        return render(request, "loginPage.html")     
    
@csrf_exempt
def loginPageForm(request):
    
    return render(request, 'loginPageForm.html')


@csrf_exempt
def healthCheck(request):
    return HttpResponse('ok')

@csrf_exempt
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')


