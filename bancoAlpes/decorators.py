from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def token_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.session["user_token"]:
            return render(request, "loginPage.html")    
        else:
            response = requests.get("http://35.190.51.156:8082/user/is_authenticated?token=" + request.session["user_token"])
            
            if "error" in response.text:
                return render(request, "loginPage.html")
            else:
                return redirect("http://34.110.196.225/indexdocumentos/?token=" + request.session["user_token"])
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func