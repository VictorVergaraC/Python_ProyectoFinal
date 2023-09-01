from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader

from .views import *

urlpatterns = [
    path('', home_productos, name="home_productos"),
    path('proteinas/', proteins, name="productos_proteinas"),
]