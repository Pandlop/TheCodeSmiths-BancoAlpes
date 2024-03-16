from django.http import HttpResponse

def home(resquest):
    return HttpResponse("Hello world, django views")