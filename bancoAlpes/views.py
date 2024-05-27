import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
import requests


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
from .decorators import token_required

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from django.core.mail import send_mail
from django.conf import settings

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization




@csrf_exempt
def landingPage(request):

    return render(request, 'landingPage.html')


@csrf_exempt
def healthCheck(request):
    return HttpResponse('ok')

@csrf_exempt
def indexDocumentos(request):
    return render(request, 'indexDocumentos.html')


