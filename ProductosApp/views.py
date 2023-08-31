from django.shortcuts import render
from .models import *

def home_productos(request):

    return render(request,
                  "productos/home.html")
    pass
