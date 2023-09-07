from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ProductosApp.models import Producto
from django.contrib.auth.decorators import login_required # para vistas basadas en funciones
import locale

@login_required
def carrito(request):
    usuario = request.user

    cliente = User.objects.filter(username=usuario).first()
    carrito = Carrito.objects.filter(cliente = cliente).first()
    
    locale.setlocale(locale.LC_ALL, 'es_CL')

    total = 0
    detalle = { }
    if carrito:
        total = locale.format_string("%d", carrito.total, grouping=True)
        detalle = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

    contexto = {
        "title"           : "Carrito de Compras",
        "carrito_detalle" : detalle,
        "mensaje"         : "",
        "total"           : total
    }
    return render(request, "CarritoApp/carrito_detalle.html", contexto)


def agregar_producto(request, id):
    
    id_producto = id
    usuario = request.user
    titulo  = "Carrito de Compras"
    if not request.user.is_authenticated:
        contexto = {
            "form"  : AuthenticationForm(),
            "title" : "Login",
            "msg"   : "Debes iniciar sesión para agregar productos al carro!"
        }
        return render(request, "proyecto_final/auth/login.html", contexto)
    else:
        msje_salida = ""

        producto = Producto.objects.filter(id = id).values('id','descripcion','precio') # obtenemos el producto
        
        producto_descripcion = ""
        producto_precio      = 0

        for item in producto:
            producto_descripcion = item['descripcion']
            producto_precio      = item['precio']

        linea_producto = 1
        existe_en_detalle = False

        cliente = User.objects.filter(username=usuario).first()
        
        carrito  = Carrito.objects.filter(cliente = cliente).first()
        total    = 0
        lineas   = 0

        if carrito:

            carrito.total += producto_precio
            carrito.save()

            carrito_detalle = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente) # obtenemos todos los productos que agregó el cliente
            
            for detalle in carrito_detalle:
                
                if detalle.id_producto.id == int(id_producto):

                    linea_producto = detalle.linea # capturamos la línea para hacerle un update a la cantidad y subtotal
                    existe_en_detalle = True

                total  += detalle.subtotal
                lineas += 1

            if existe_en_detalle: # Actualizamos la cantidad y sub total
                linea_producto = CarritoDetalle.objects.filter(linea = linea_producto, id_producto = id).first()
                linea_producto.cantidad += 1
                linea_producto.subtotal += producto_precio
                linea_producto.save()
                msje_salida = "Carrito actualizado!"
            else: # agregamos una nueva linea
                lineas += 1
                new_linea = CarritoDetalle(
                                            id_carrito  = carrito, # Se pasa el carrito como instancia
                                            cliente     = cliente, 
                                            linea       = lineas,
                                            id_producto = get_object_or_404(Producto, id=id),
                                            precio      = producto_precio,
                                            cantidad    = 1,
                                            subtotal    = producto_precio)
                new_linea.save()
                msje_salida = "Producto agregado!"

            locale.setlocale(locale.LC_ALL, 'es_CL')
            total = locale.format_string("%d", carrito.total, grouping=True)
            contexto = {
                "title"           : titulo,
                "carrito_detalle" : CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto'),
                "mensaje"         : msje_salida,
                "total"           : total,
                "id_carrito"      : int(carrito.id)
            }
            return render(request, "CarritoApp/carrito_detalle.html", contexto)
        else:
            # no existe carrito
            new_carrito = Carrito(cliente = cliente, total = producto_precio)
            new_carrito.save()
            id_new = new_carrito.id

            new_detalle = CarritoDetalle(
                                            id_carrito  = new_carrito,
                                            cliente     = cliente,
                                            linea       = 1,
                                            id_producto = get_object_or_404(Producto, id=id),
                                            precio      = producto_precio,
                                            cantidad    = 1,
                                            subtotal    = producto_precio)
            new_detalle.save()
            msje_salida = f"Nuevo carrito creado, agregamos el producto '{producto_descripcion}'!"

            locale.setlocale(locale.LC_ALL, 'es_CL')
            total = locale.format_string("%d", new_carrito.total, grouping=True)

            contexto = {
                "title"           : titulo,
                "carrito_detalle" : CarritoDetalle.objects.filter(id_carrito = id_new, cliente = cliente),
                "mensaje"         : msje_salida,
                "total"           : total,
                "id_carrito"      : int(id_new)
            }
            return render(request, "CarritoApp/carrito_detalle.html", contexto)


def modificar_cantidad(request, id, linea, accion):

    pass

def imprime(descripcion, parametro):
    print()
    print()
    print(descripcion, parametro)
    print()
    print()
