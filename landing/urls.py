from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.landingPage, name='landingPage'),
    path('landingPage', views.landingPage, name='landingPage'),

]