from django.urls import path, include
from .views import *
from proyecto_final.views import login_request

# app_name = 'ProductosApp'

urlpatterns = [
    path('proteinas/', proteins, name="productos_proteinas"),
    path('creatinas/', creatines, name="productos_creatinas"),
    path('otros/', otros, name="productos_otros"),
    path('prueba/', login_request, name="login_request"),
]