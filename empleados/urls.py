from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('vistaDocs/', views.vistaDocs, name='vistaDocs'),
    path('logout/', views.logout_view, name='logout_view'),
    path('aprobar/<int:id>', views.aprobar, name='aprobar'),
    path('rechazar/<int:id>', views.rechazar, name='rechazar'),
]