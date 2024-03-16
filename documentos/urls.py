from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('documentosCarga', views.documentosCarga_view, name='documentosCarga_view'),
    path('documentosCarga/<int:doc_pk>', views.documentoCarga_view, name='documentoCarga_view')
]