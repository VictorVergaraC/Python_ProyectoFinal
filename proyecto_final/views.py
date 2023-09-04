from django.shortcuts import render, redirect
from ProductosApp.views import home_productos
from ProductosApp.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            username = data["username"]
            clave    = data["password"]

            usuario = authenticate(username=username, password=clave)

            if usuario is not None:
                login(request, usuario)
                return render(request, "", {})

            
    # else
    form = AuthenticationForm()

    context = {
        "form" :form,
        "title": "Login",
        "msg"  : ""
    }
    
    return render(request ,"login.html", context)