from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ProductosApp.models import Producto
from CompraApp.models import Compra, CompraDetalle
from django.contrib.auth.decorators import login_required # para vistas basadas en funciones
import locale
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

def imprime(descripcion, parametro):
    print()
    print()
    print(descripcion, parametro)
    print()
    print()

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

def comentario(request, id):
    usuario = request.user
    cliente, created = User.objects.get_or_create(username=usuario)

    producto = Producto.objects.filter(id=id).first()

    if request.method == "POST":

        descripcion = request.POST["descripcion"].capitalize()

        new_comentario = ComentarioProducto(
            descripcion = descripcion,
            id_producto = producto,
            cliente     = cliente,
            fecha       = timezone.now().date())
        new_comentario.save()

        contexto = {
            "title"       : "Agregar Comentario",
            "comentarios" : ComentarioProducto.objects.filter(id_producto=producto).order_by('-fecha').select_related('id_producto'),
            "mensaje"     : "Comentario Agregado!",
            "producto"    : producto
        }
        return render(request, "ProductosApp/productos/comentario/comentario.html", contexto)

    
    contexto = {
        "title"       : "Agregar Comentario",
        "comentarios" : ComentarioProducto.objects.filter(id_producto=producto).order_by('-fecha').select_related('id_producto','cliente'),
        "producto"    : producto
    }
    return render(request, "ProductosApp/productos/comentario/comentario.html", contexto)

@login_required
def administrar_productos(request):
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if not usuario.is_superuser:
        return redirect('home_productos')

    contexto = {
        "title" : "Administrar Productos",
        "productos" : Producto.objects.all().select_related('categoria')
    }
    return render(request, "ProductosApp/admin/listado_productos.html", contexto)

@login_required
def editar_producto(request, id):
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if not usuario.is_superuser:
        return redirect('home_productos')

    producto   = Producto.objects.filter(id = id).select_related('categoria').first()
    categorias = Categoria.objects.all()

    if request.method == "POST":

        imagen       = request.FILES['imagen']
        descripcion  = request.POST['descripcion']
        id_categoria = request.POST['categoria']
        precio       = request.POST['precio']

        # Validaciones ...
        if int(precio) <= 0:
            img_temp = ProductoImg.objects.filter(id_producto = producto).first()
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp if img_temp else "/media/products/default.png",
                "mensaje"    : "El precio no puede ser menor o igual a 0!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        if descripcion == '' or len(descripcion) <= 4:
            img_temp = ProductoImg.objects.filter(id_producto = producto).first()
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp if img_temp else "/media/products/default.png",
                "mensaje"    : "Descripción muy corta!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        if not Categoria.objects.filter(id = id_categoria).first():
            img_temp = ProductoImg.objects.filter(id_producto = producto).first()
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp if img_temp else "/media/products/default.png",
                "mensaje"    : "La categoría no existe!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        # Fin de validaciones ...

        categoria_producto   = Categoria.objects.filter(id = id_categoria).first()
        producto.descripcion = descripcion.upper()
        producto.categoria   = categoria_producto
        producto.precio      = int(precio)
        producto.save()

        msg_producto = "Producto actualizado!"
        msg_imagen   = ""

        img = ProductoImg.objects.filter(id_producto = producto).first()
        if img:
            img.imagen = imagen
            img.save()
            msg_imagen = "Imagen actualizada!"
        else:
            new_img = ProductoImg(imagen = imagen, id_producto = producto)
            new_img.save()
            msg_imagen = "Imagen agregada!"
        
        contexto = {
            "title"      : f"Editar: {producto.descripcion}",
            "producto"   : producto,
            "categorias" : categorias,
            
        }

    imagen = ProductoImg.objects.filter(id_producto = producto).first()

    if not imagen:
        imagen = "/media/products/default.png"

    contexto = {
        "title"      : f"Editar: {producto.descripcion}",
        "producto"   : producto,
        "categorias" : categorias,
        "img"        : imagen
    }

    return render(request, "ProductosApp/admin/editar_producto.html", contexto)

def GetImagen(id):
    img = ProductoImg.objects.filter(id = id)
    if len(img) != 0:
        return img[0].imagen.url
    
    return "/media/products/default.png"
