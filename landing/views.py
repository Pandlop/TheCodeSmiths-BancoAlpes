import json
from django.shortcuts import render

# Create your views here.
def landingPage(request):
    
    print(request.session["login_info"])
    print(request.user)
    
    estaLogueado = request.session.get("user") != None;
    
    context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4), 'estaLogueado': estaLogueado}
    return render(request, 'landingPage.html', context)