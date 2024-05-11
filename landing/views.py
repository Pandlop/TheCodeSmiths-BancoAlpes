import json
from django.shortcuts import render, redirect

from empleados.models import Empleado

# Create your views here.
def landingPage(request):
    
    print("Estoy en el landingPage de landing views.py")

    
#     print(request.session.get("loginInfo"))
    
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
