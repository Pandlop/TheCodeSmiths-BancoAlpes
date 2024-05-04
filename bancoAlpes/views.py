import os
from time import sleep
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .forms import Login_Info
import requests
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from urllib.parse import quote_plus, urlencode
from django.views.decorators.csrf import csrf_exempt
from time import sleep



# Cosas de autenticación -------------------------------------------------------


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
@csrf_exempt
def login(request):
    print(request.session.get("login_info"), "desde login")
    
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback")),
        connection = "sms",
    )

@csrf_exempt
def callback(request):
    token = oauth.auth0.authorize_access_token(request)

    request.session["user"] = token

    print("ya estoy saliendo del callback")

    return redirect(request.build_absolute_uri(reverse("loginPage")))

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
    return redirect(reverse("login"))


# Otras funciones ---------------------------------------------------------------

@csrf_exempt
def landingPage(request):    

    return render(request, 'landingPage.html')

@csrf_exempt
def loginPage(request):

    return render(request, 'loginPage.html')
    
@csrf_exempt
def loginPageForm(request):
    
    return render(request, 'loginPageForm.html')


@csrf_exempt
def healthCheck(request):
    return HttpResponse('ok')

@csrf_exempt
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')