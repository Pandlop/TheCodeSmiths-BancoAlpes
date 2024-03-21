from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexDocumentos, name='indexDocumentos'),
    path('documentosCarga/', views.list_docs, name='list_docs'),
    path('files/', views.file_list, name='file_list'),
    path('docsFallidos/', views.docsFallidos, name='docsFallidos'),
]