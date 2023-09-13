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
import os
from django.conf import settings

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
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'home_productos'
    }
    
    return render(request, "ProductosApp/productos/home/home_contenido.html", context)
    
def proteins(request):
    pageTitle = "Proteínas"
    titleSection = "Todo en Proteínas"

    message   = ""
    allProducts = Producto.objects.filter(categoria = 1)

    products    = True
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'productos_proteinas'
    }

    return render(request, "ProductosApp/productos/home/home_contenido.html", context)

def creatines(request):
    pageTitle = "Creatinas"
    titleSection = "Todo en Creatinas"

    message   = ""
    allProducts = Producto.objects.filter(categoria = 2)

    products    = True
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'productos_creatinas'
    }

    return render(request, "ProductosApp/productos/home/home_contenido.html", context)

def otros(request):
    pageTitle = "Otros Productos"
    titleSection = "Todo en Otros Productos"

    message   = ""
    allProducts = Producto.objects.exclude(Q(categoria=1) | Q(categoria=2))

    products    = True
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'productos_otros'
    }

    return render(request, "ProductosApp/productos/home/home_contenido.html", context)

def todos(request):
    pageTitle = "Todos Nuestros Productos"
    titleSection = "Nuestros Productos"

    message   = ""
    allProducts = Producto.objects.all()

    products    = True
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'productos_otros'
    }

    return render(request, "ProductosApp/productos/home/home_contenido.html", context)

def accesorios(request):
    pageTitle = "Accesorios"
    titleSection = "Todo en Accesorios"

    message   = ""
    allProducts = Producto.objects.filter(categoria = 4)

    products      = True
    productos_img = []

    locale.setlocale(locale.LC_ALL, 'es_CL')
    if not allProducts:
        message  = "No existen productos! :("
        products = False
    else:
        for product in allProducts:
            imagen = ProductoImg.objects.filter(id_producto = product).first()
            product.precio = locale.format_string("%d", product.precio, grouping=True)
            productos_img.append({
                "product": product,
                "imagen": imagen.imagen
            })

    context = {
        "title"       : pageTitle,
        "titleSection": titleSection,
        "msg"         : message,
        "products"    : products,
        "allProducts" : productos_img if len(allProducts) > 0 else allProducts,
        "redirect"    : 'productos_proteinas'
    }

    return render(request, "ProductosApp/productos/home/home_contenido.html", context)

def comentario(request, id):
    usuario = request.user
    cliente, created = User.objects.get_or_create(username=usuario)

    producto = Producto.objects.filter(id=id).first()
    img = ProductoImg.objects.filter(id_producto = producto).first()
    
    locale.setlocale(locale.LC_ALL, 'es_CL')

    if request.method == "POST":

        descripcion = request.POST["descripcion"].capitalize()

        new_comentario = ComentarioProducto(
            descripcion = descripcion,
            id_producto = producto,
            cliente     = cliente,
            fecha       = timezone.now().date())
        new_comentario.save()

        producto.precio = locale.format_string("%d", producto.precio, grouping=True)
        contexto = {
            "title"       : "Agregar Comentario",
            "comentarios" : ComentarioProducto.objects.filter(id_producto=producto).order_by('-fecha').select_related('id_producto'),
            "mensaje"     : "Comentario Agregado!",
            "producto"    : producto,
            "img"         : img.imagen.url if img.imagen else "products/default.png"
        }
        return render(request, "ProductosApp/productos/comentario/comentario.html", contexto)

    producto.precio = locale.format_string("%d", producto.precio, grouping=True)
    contexto = {
        "title"       : "Agregar Comentario",
        "comentarios" : ComentarioProducto.objects.filter(id_producto=producto).order_by('-fecha').select_related('id_producto','cliente'),
        "producto"    : producto,
        "img"         : img.imagen.url if img.imagen else "products/default.png"
    }
    return render(request, "ProductosApp/productos/comentario/comentario.html", contexto)

@login_required
def administrar_productos(request):
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if not usuario.is_superuser:
        return redirect('home_productos')
    
    locale.setlocale(locale.LC_ALL, 'es_CL')
    productos_img = []
    allProducts = Producto.objects.all().select_related('categoria')
    for producto in allProducts:
        img = ProductoImg.objects.filter(id_producto = producto).first()
        producto.precio = locale.format_string("%d", producto.precio, grouping=True)
        productos_img.append({
            "producto" : producto,
            "img"      : img.imagen
        })


    contexto = {
        "title" : "Administrar Productos",
        "productos" : productos_img
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
        # capturamos los datos         
        param_img    = request.FILES['imagen'] if len(request.FILES) else ""
        descripcion  = request.POST['descripcion'].strip()
        id_categoria = request.POST['categoria']
        precio       = request.POST['precio']

        # Validaciones ...
        img_temp = ProductoImg.objects.filter(id_producto = producto).first()
        if int(precio) <= 0:
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp.imagen.url if img_temp else "/media/products/default.png",
                "mensaje"    : "El precio no puede ser menor o igual a 0!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        if descripcion == '' or len(descripcion) <= 4:
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp.imagen.url if img_temp else "/media/products/default.png",
                "mensaje"    : "Descripción muy corta!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        if not Categoria.objects.filter(id = id_categoria).first():
            contexto = {
                "title"      : f"Editar: {producto.descripcion}",
                "producto"   : producto,
                "categorias" : categorias,
                "img"        : img_temp.imagen.url if img_temp else "/media/products/default.png",
                "mensaje"    : "La categoría no existe!"
            }
            return render(request, "ProductosApp/admin/editar_producto.html", contexto)
        
        # Fin de validaciones ...

        # Actualizamos el producto ...
        categoria_producto   = Categoria.objects.filter(id = id_categoria).first()
        producto.descripcion = descripcion.upper()
        producto.categoria   = categoria_producto
        producto.precio      = int(precio)
        producto.save()

        msg_producto = "Producto actualizado!"
        
        # Validamos si el cliente subió una imagen para agregarla o actualizarla ...
        img = ProductoImg.objects.filter(id_producto = producto).first()
        if not img:
            img = ProductoImg(
                imagen="products/default.png" if param_img == "" else param_img,
                id_producto=producto
            )
            msg_producto += " e Imagen agregada!"
        elif not img.imagen:
            img.imagen = "products/default.png" if param_img == "" else param_img
        else:
            
            if "default" in str(img.imagen):
                img.imagen = "products/default.png" if param_img == "" else param_img                
            else:
                imprime("no contiene default","")
                if param_img != "" and param_img != "":
                    img.imagen = param_img
                    msg_producto += " e Imagen actualizada!"
                # end if
            # end if
        img.save()
                
        img = ProductoImg.objects.filter(id_producto = producto).first()
        contexto = {
            "title"      : f"Editar: {producto.descripcion}",
            "producto"   : producto,
            "categorias" : categorias,
            "img"        : img.imagen.url,
            "mensaje"    : msg_producto
        }
        return render(request, "ProductosApp/admin/editar_producto.html", contexto)

    imagen = ProductoImg.objects.filter(id_producto = producto).first()

    contexto = {
        "title"      : f"Editar: {producto.descripcion}",
        "producto"   : producto,
        "categorias" : categorias,
        "img"        : imagen.imagen.url if imagen else "/media/products/default.png"
    }

    return render(request, "ProductosApp/admin/editar_producto.html", contexto)

@login_required
def eliminar_producto(request, id):
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if not usuario.is_superuser:
        return redirect('home_productos')

    producto = Producto.objects.get(id = id)
    producto_img = ProductoImg.objects.filter(id_producto = producto)

    for img in producto_img:
        img.imagen.delete()
        img.delete()

    producto.delete()

    locale.setlocale(locale.LC_ALL, 'es_CL')
    productos_img = []
    allProducts = Producto.objects.all().select_related('categoria')
    for producto in allProducts:
        img = ProductoImg.objects.filter(id_producto = producto).first()
        producto.precio = locale.format_string("%d", producto.precio, grouping=True)
        productos_img.append({
            "producto" : producto,
            "img"      : img.imagen
        })

    contexto = {
        "title"     : "Administrar Productos",
        "productos" : productos_img,
        "mensaje"   : "Producto eliminado correctamente!"
    }
    return render(request, "ProductosApp/admin/listado_productos.html", contexto)


@login_required
def crear_producto(request):
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if not usuario.is_superuser:
        return redirect('home_productos')
    
    categorias = Categoria.objects.all()

    if request.method == "POST":

        imprime("len:", len(request.FILES))

        param_img    = request.FILES['imagen'] if len(request.FILES) > 0 else ""
        descripcion  = request.POST['descripcion'].strip()
        id_categoria = request.POST['categoria']
        precio       = int(request.POST['precio'])

        categoria = Categoria.objects.filter(id = int(id_categoria)).first()

        mensaje = ""
        errores = False
        # Validaciones
        if descripcion == "" or len(descripcion) <= 5:
            mensaje = "Descripción muy corta!"
            errores = True
        if precio <= 0:
            mensaje = "El precio no puede ser menor a 1"
            errores = True
        if not categoria:
            mensaje = "La categoría no existe!"
            errores = True
        
        if errores == True:
            contexto = {
                "title"      : "Administrar Productos!",
                "categorias" : categorias,
                "mensaje"    : mensaje
            }
            return render(request, "ProductosApp/admin/crear_producto.html", contexto)
        # Fin validaciones ...

        new_producto = Producto(
            descripcion   = descripcion.upper(),
            categoria     = categoria,
            precio        = precio,
            oferta        = False,
            precio_oferta = 0,
            activo        = True
        )
        new_producto.save()

        new_producto_img = ProductoImg(
            imagen      = "products/default.png" if param_img == "" else param_img,
            id_producto = new_producto
        )
        new_producto_img.save()

        locale.setlocale(locale.LC_ALL, 'es_CL')
        productos_img = []
        allProducts = Producto.objects.all().select_related('categoria')
        for producto in allProducts:
            img = ProductoImg.objects.filter(id_producto = producto).first()
            producto.precio = locale.format_string("%d", producto.precio, grouping=True)
            productos_img.append({
                "producto" : producto,
                "img"      : img.imagen
            })

        contexto = {
            "title"     : "Administrar Productos",
            "productos" : productos_img,
            "mensaje"   : "Producto creado satisfactoriamente!"
        }
        return render(request, "ProductosApp/admin/listado_productos.html", contexto)


    contexto = {
        "title"      : "Crear Producto!",
        "categorias" : categorias
    }

    return render(request, "ProductosApp/admin/crear_producto.html", contexto)