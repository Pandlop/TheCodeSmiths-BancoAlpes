import json
from django.shortcuts import render, redirect

# Create your views here.
def landingPage(request):
    return render(request, 'landingPage.html')
