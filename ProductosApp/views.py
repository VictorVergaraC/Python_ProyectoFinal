from django.shortcuts import render
from .models import *

def home_productos(request):
    pageTitle   = "Bienvenido!"
    titleSection = "Todos nuestros productos"

    message = ""
    allProducts = Producto.objects.all()
    
    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"      : pageTitle,
        "titleSection": titleSection,
        "msg"        : message,
        "products"   : products,
        "allProducts": allProducts
    }

    return render(request,
                  "productos/home/home_contenido.html",
                  context)
    
def proteins(request):
    pageTitle = "Proteínas"
    titleSection = "Todo en Proteínas"

    message   = ""
    allProducts = Producto.objects.filter(categoria = 1)

    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : allProducts
    }

    return render(request,
                  "productos/home/home_contenido.html",
                  context)


    pass
