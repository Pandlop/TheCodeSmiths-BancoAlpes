"""
URL configuration for bancoAlpes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    # URS's de autenticacion -----------------------------------------------------
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('logout/', views.logout, name='logout'),
    # Otras URL's ----------------------------------------------------------------
    path('indexDocumentos/', views.indexDocumentos, name='indexDocumentos'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('loginPage/loginPageForm/', views.loginPageForm, name='loginPageForm'),
    path('loginPage/loginPageForm/submit_login_info/', views.submit_login_info, name='submit_login_info'),

    path('admin/', admin.site.urls),
    path('documentos/', include('documentos.urls')),
    path('landingPage/', include('landing.urls')),
    path('empleados/', include('empleados.urls')),
    path('solicitudes/', include('solicitudes.urls')),
    path('health-check/', views.healthCheck),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)