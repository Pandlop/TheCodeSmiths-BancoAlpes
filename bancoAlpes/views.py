import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
import requests

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
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


@csrf_exempt
def landingPage(request):
    return render(request, 'landingPage.html')

@csrf_exempt
def healthCheck(request):
    return HttpResponse('ok')

@csrf_exempt
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')


