from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', carrito, name='carrito'),
    path('agregar_al_carro/<id>', agregar_producto, name='agregar_al_carro'),
    path('modificar_cantidad/<id>/<linea>/<str:accion>/', modificar_cantidad, name='sumar_cantidad'),
    path('finalizar', pre_finalizar_pedido, name='pre_finalizar_pedido'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
