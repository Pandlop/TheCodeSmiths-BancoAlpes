from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# def index(request):
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render())

@csrf_exempt
def landingPage(request):
    return render(request, 'landingPage.html')

@csrf_exempt
def healthCheck(request):
    return HttpResponse('ok')