from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def carrito(request):

    pass

def agregar_producto(request, id):
    usuario = request.user
    if usuario == "AnonymousUser":
        return redirect('login_request')
    else:
        pass

def pago(request):

    pass
