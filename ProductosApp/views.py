from django.shortcuts import render
from django.db.models import Q
from .models import *

def home_productos(request):
    pageTitle   = "Bienvenido!"
    titleSection = "Todos nuestros productos"

    message = ""
    allProducts = Producto.objects.all()[:10] # Con [:10] se agrega un límite de 10 registros
    
    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : allProducts,
        "redirect"    : 'home_productos'
    }
    
    return render(request,
                  "ProductosApp/productos/home/home_contenido.html",
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
        "allProducts" : allProducts,
        "redirect"    : 'productos_proteinas'
    }

    return render(request,
                  "ProductosApp/productos/home/home_contenido.html",
                  context)

def creatines(request):
    pageTitle = "Creatinas"
    titleSection = "Todo en Creatinas"

    message   = ""
    allProducts = Producto.objects.filter(categoria = 2)

    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : allProducts,
        "redirect"    : 'productos_creatinas'
    }

    return render(request,
                  "ProductosApp/productos/home/home_contenido.html",
                  context)

def otros(request):
    pageTitle = "Otros Productos"
    titleSection = "Todo en Otros Productos"

    message   = ""
    allProducts = Producto.objects.exclude(Q(categoria=1) | Q(categoria=2))

    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : allProducts,
        "redirect"    : 'productos_otros'
    }

    return render(request,
                  "ProductosApp/productos/home/home_contenido.html",
                  context)

def todos(request):
    pageTitle = "Todos Nuestros Productos"
    titleSection = "Nuestros Productos"

    message   = ""
    allProducts = Producto.objects.all()

    products    = True
    if not allProducts:
        message  = "No existen productos! :("
        products = False

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : allProducts,
        "redirect"    : 'productos_otros'
    }

    return render(request,
                  "ProductosApp/productos/home/home_contenido.html",
                  context)
