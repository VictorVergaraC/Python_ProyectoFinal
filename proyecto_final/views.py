from django.shortcuts import render, redirect
from ProductosApp.views import home_productos
from ProductosApp.models import *
from CompraApp.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import *
from .models import *
import locale
from django.contrib.auth.decorators import login_required # para vistas basadas en funciones

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data["username"]
            clave = data["password"]

            usuario = authenticate(username=username, password=clave)

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
                "title"        : "Home",
                "titleSection" : "Todos nuestros productos",
                "msg"          : message,
                "mensaje"      : f"Usuario {username} logueado correctamente!",
                "products"     : products,
                "allProducts"  : productos_img if len(allProducts) > 0 else allProducts
            }
            if usuario is not None:
                login(request, usuario)
                return render(request, "ProductosApp/productos/home/home_contenido.html", context)

            # else ...
            context = {
                "form"  : AuthenticationForm(),
                "title" : "Login",
                "msg"   : "Credenciales inválidas!"
            }
            return render(request, "proyecto_final/auth/login.html", context)
        # else ...
        context = {
            "form"  : AuthenticationForm(),
            "title" : "Login",
            "msg"   : "Datos inválidos!"
        }
        return render(request, "proyecto_final/auth/login.html", context)

    # else ...
    form = AuthenticationForm()

    context = {
        "form"  : form,
        "title" : "Login",
        "msg"   : ""
    }

    return render(request, "proyecto_final/auth/login.html", context)

@login_required
def mis_datos(request):
    user    = request.user
    usuario = User.objects.filter(username=user).values('first_name', 'last_name','email')
    
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.email      = data["email"]
            user.password1  = data["password1"]
            user.password2  = data["password2"]
            user.first_name = data["first_name"]
            user.last_name  = data["last_name"]
            user.save()

            contexto = {
               "title"    : "Mis Datos",
                "usuario" : usuario,
                "form"    : UserEditForm() ,
                "msje"    : "Datos actualizados correctamente!"
            }
            return render(request, "proyecto_final/auth/mis_datos.html", contexto)


    context = {
        "title"   : "Mis Datos",
        "usuario" : usuario,
        "form"    : UserEditForm()
    }
    return render(request, "proyecto_final/auth/mis_datos.html", context)

def registrarme(request):
    
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            message = ""
            allProducts = Producto.objects.all()[:10] # Con [:10] se agrega un límite de 10 registros
            products    = True
            if not allProducts:
                message  = "No existen productos! :("
                products = False

            contexto = {
                "title"         : "Home",
                "titleSection"  : "Todos nuestros productos",
                "msg"           : message,
                "mensaje"       : f"Bienvenido {user}, creaste una cuenta y fuiste logueado!",
                "products"      : products,
                "allProducts"   : allProducts
            }

            return render(request,"ProductosApp/productos/home/home_contenido.html", contexto)
        
        contexto = {
            "title" : "Login",
            "form"  : RegistroUsuarioForm(),
            "msg"   : form.errors
        }
        return render(request, "proyecto_final/auth/registro_usuario.html", contexto)

    contexto = {
        "title" : "Registrarme",
        "form"  : RegistroUsuarioForm()
    }
    return render(request, "proyecto_final/auth/registro_usuario.html", contexto)

@login_required
def mis_compras(request):
    usuario = request.user
    cliente = User.objects.filter(username=usuario).first()

    locale.setlocale(locale.LC_ALL, 'es_CL')
    
    compras = Compra.objects.filter(cliente = cliente).values('id','total','fecha')
    for product in compras:
        imprime("product:", product)
        product['total'] = locale.format_string("%d", product['total'], grouping=True)
        product['fecha'] = product['fecha'].strftime('%d/%m/%Y')

    contexto = {
        "title" : "Mis Compras",
        "compras" : compras
    }

    return render(request, "ComprasApp/mis_compras.html", contexto)


def imprime(descripcion, parametro):
    print()
    print()
    print(descripcion, parametro)
    print()
    print()