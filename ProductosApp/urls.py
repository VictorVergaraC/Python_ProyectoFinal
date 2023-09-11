from django.urls import path, include
from .views import *
from proyecto_final.views import login_request

# app_name = 'ProductosApp'

urlpatterns = [
    path('proteinas/', proteins, name="productos_proteinas"),
    path('creatinas/', creatines, name="productos_creatinas"),
    path('otros/', otros, name="productos_otros"),
    path('todos/', todos, name="productos_todos"),
    path('comentar/<id>/', comentario, name="comentar_producto"),
]