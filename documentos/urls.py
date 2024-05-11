from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexDocumentos, name='indexDocumentos'),
    path('documentosCarga/', views.list_docs, name='list_docs'),
    path('documentosCarga/<int:docId>', views.list_docs_id, name='list_docs_id'),
    # path('upload/', views.upload_document, name='upload_document'),
    # path('verify/<int:doc_id>/', views.verify_document, name='verify_document'),
]