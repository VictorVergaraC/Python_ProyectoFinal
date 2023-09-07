from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ProductosApp.models import Producto

def carrito(request):

    pass

def agregar_producto(request, id):
    usuario = request.user
    titulo  = "Carrito de Compras"
    if usuario == "AnonymousUser":
        contexto = {
            "form"  : AuthenticationForm(),
            "title" : "Login",
            "msg"   : "Debes iniciar sesión para agregar productos al carro!"
        }
        return render(request, "proyecto_final/auth/login.html", contexto)
    else:
        msje_salida = ""

        producto_ins = get_object_or_404(Producto, id=id)

        producto = Producto.objects.filter(id = id).values('id','descripcion','precio') # obtenemos el producto
                
        producto_id          = 0
        producto_descripcion = ""
        producto_precio      = 0

        for item in producto:
            producto_id          = item['id']
            producto_descripcion = item['descripcion']
            producto_precio      = item['precio']

        linea_producto = 1
        existe_en_detalle = False

        carrito  = Carrito.objects.filter(cliente = usuario).first()
        total    = 0
        lineas   = 0

        if carrito:
            carrito.total += producto_precio
            carrito.save()

            carrito_detalle = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = usuario) # obtenemos todos los productos que agregó el cliente
        
            for detalle in carrito_detalle:

                if detalle.id_producto == id:
                    linea_producto = detalle.linea # capturamos la línea para hacerle un update a la cantidad y subtotal
                    existe_en_detalle = True

                total  += detalle.subtotal
                lineas += 1
            
            if existe_en_detalle: # Actualizamos la cantidad y sub total
                linea_producto = CarritoDetalle.objects.filter(linea = linea_producto, id_producto = id)
                linea_producto.cantidad += 1
                linea_producto.subtotal += producto_precio
                linea_producto.save()
                msje_salida = "Carrito actualizado!"
            else: # agregamos una nueva linea
                lineas += 1
                new_linea = CarritoDetalle(
                                            id_carrito  = carrito,
                                            cliente     = usuario, 
                                            linea       = lineas,
                                            id_producto = producto_ins,
                                            precio      = producto_precio,
                                            cantidad    = 1,
                                            subtotal    = producto_precio)
                new_linea.save()
                msje_salida = "Producto agregado!"
            detalles = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = usuario)
            detalles = detalles.select_related('id_producto')

            for item in detalles:
                # item.linea item.id_producto.descripcion, item.precio, item.cantidad
                imprime("detalle:", f"{item.linea}, {item.id_producto.descripcion}, {item.precio}, {item.cantidad}")

            contexto = {
                "carrito_detalle" : detalles,
                "mensaje"         : msje_salida,
            }
            return render(request, "CarritoApp/carrito_detalle.html", contexto)
        else:
            # no existe carrito
            new_carrito = Carrito(cliente = usuario, total = producto_precio)
            new_carrito.save()
            id_new = new_carrito.id

            new_detalle = CarritoDetalle(
                                            id_carrito  = new_carrito,
                                            cliente     = usuario,
                                            linea       = 1,
                                            id_producto = producto_ins,
                                            precio      = producto_precio,
                                            cantidad    = 1,
                                            subtotal    = producto_precio)
            new_detalle.save()
            msje_salida = f"Nuevo carrito creado, agregamos el producto '{producto_descripcion}'!"

            contexto = {
                "carrito_detalle" : CarritoDetalle.objects.filter(id_carrito = id_new, cliente = usuario),
                "mensaje"         : msje_salida,
            }
            return render(request, "CarritoApp/carrito_detalle.html", contexto)
        
        

def imprime(descripcion, parametro):
    print()
    print()
    print(descripcion, parametro)
    print()
    print()
