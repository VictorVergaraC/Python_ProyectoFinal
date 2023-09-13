from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ProductosApp.models import Producto, ProductoImg
from CompraApp.models import Compra, CompraDetalle
from django.contrib.auth.decorators import login_required # para vistas basadas en funciones
import locale
from datetime import datetime
from django.utils import timezone

@login_required
def carrito(request):
    usuario = request.user

    cliente = User.objects.filter(username=usuario).first()
    carrito = Carrito.objects.filter(cliente = cliente).first()
    
    locale.setlocale(locale.LC_ALL, 'es_CL')

    total = 0

    producto_img = []

    if carrito:
        total = locale.format_string("%d", carrito.total, grouping=True)
        allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

        for item in allProducts:
            
            imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

            producto_img.append({
                "img"         : imagen.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.precio, grouping=True),
                "cantidad"    : item.cantidad,
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                "id_carrito"  : item.id_carrito
            })
    
    contexto = {
        "title"           : "Carrito de Compras",
        "carrito_detalle" : producto_img,
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

        locale.setlocale(locale.LC_ALL, 'es_CL')
        
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

            allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')
            producto_img = []

            for item in allProducts:
            
                imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

                producto_img.append({
                    "img"         : imagen.imagen,
                    "linea"       : item.linea,
                    "id_producto" : item.id_producto,
                    "precio"      : locale.format_string("%d", item.precio, grouping=True),
                    "cantidad"    : item.cantidad,
                    "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                    "id_carrito"  : item.id_carrito
                })
            
            total = locale.format_string("%d", carrito.total, grouping=True)
            contexto = {
                "title"           : titulo,
                # "carrito_detalle" : CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto'),
                "carrito_detalle" : producto_img,
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

            total = locale.format_string("%d", new_carrito.total, grouping=True)

            allProducts = CarritoDetalle.objects.filter(id_carrito = new_carrito, cliente = cliente).select_related('id_producto')
            producto_img = []
            
            if len(allProducts) > 0:
                for item in allProducts:
            
                    imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

                    producto_img.append({
                        "img"         : imagen.imagen,
                        "linea"       : item.linea,
                        "id_producto" : item.id_producto,
                        "precio"      : locale.format_string("%d", item.precio, grouping=True),
                        "cantidad"    : item.cantidad,
                        "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                        "id_carrito"  : item.id_carrito
                    })
            
            total = locale.format_string("%d", carrito.total, grouping=True)
            contexto = {
                "title"           : titulo,
                # "carrito_detalle" : CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto'),
                "carrito_detalle" : producto_img,
                "mensaje"         : msje_salida,
                "total"           : total,
                "id_carrito"      : int(id_new)
            }
            return render(request, "CarritoApp/carrito_detalle.html", contexto)


def modificar_cantidad(request, id, linea, accion):
    usuario = request.user
    cliente = User.objects.get(username = usuario)
    cliente = User.objects.filter(username=usuario).first()
        
    carrito = Carrito.objects.filter(id = int(id), cliente = cliente).first()
    detalle = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente) 

    linea_detalle  = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente, linea = int(linea)).first()

    producto = Producto.objects.filter(id = linea_detalle.id_producto.id).first()
    
    locale.setlocale(locale.LC_ALL, 'es_CL')

    if accion == "restar":

        if linea_detalle.cantidad > 1:
            carrito.total -= producto.precio
            carrito.save()

            linea_detalle.cantidad -= 1
            linea_detalle.subtotal -= producto.precio
            linea_detalle.save()

            producto_img = []
            allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

            for item in allProducts:
            
                imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

                producto_img.append({
                    "img"         : imagen.imagen,
                    "linea"       : item.linea,
                    "id_producto" : item.id_producto,
                    "precio"      : locale.format_string("%d", item.precio, grouping=True),
                    "cantidad"    : item.cantidad,
                    "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                    "id_carrito"  : item.id_carrito
                })

            contexto = {
                "Title"           : "Carrito de Compras",
                "carrito_detalle" : producto_img,
                "mensaje"         : "Cantidad actualizada! Hemos quitado una unidad",
                "total"           : locale.format_string("%d", carrito.total, grouping=True),
                "id_carrito"      : carrito.id
            }

            return render(request, "CarritoApp/carrito_detalle.html", contexto)
        
        producto_img = []
        allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

        for item in allProducts:
            
            imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

            producto_img.append({
                "img"         : imagen.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.precio, grouping=True),
                "cantidad"    : item.cantidad,
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                "id_carrito"  : item.id_carrito
            })

            contexto = {
                "Title"           : "Carrito de Compras",
                "carrito_detalle" : producto_img,
                "mensaje"         : "Ya lleva la cantidad mínima, si quiere quitar el producto, por favor click en su respectivo botón!",
                "total"           : locale.format_string("%d", carrito.total, grouping=True),
                "id_carrito"      : carrito.id
        }
        return render(request, "CarritoApp/carrito_detalle.html", contexto)

    elif accion == "agregar":
        carrito.total += producto.precio
        carrito.save()

        linea_detalle.cantidad += 1
        linea_detalle.subtotal += producto.precio
        linea_detalle.save()

        producto_img = []
        allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

        for item in allProducts:
            
            imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

            producto_img.append({
                "img"         : imagen.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.precio, grouping=True),
                "cantidad"    : item.cantidad,
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                "id_carrito"  : item.id_carrito
            })
        
        contexto = {
                "title"           : "Carrito de Compras",
                "carrito_detalle" : producto_img,
                "mensaje"         : "Cantidad actualizada! Hemos agregado una unidad",
                "total"           : locale.format_string("%d", carrito.total, grouping=True),
                "id_carrito"      : carrito.id
        }

        return render(request, "CarritoApp/carrito_detalle.html", contexto)

    elif accion == "quitar": # quitar
        mensaje = "Producto eliminado!"
        carrito.total -= linea_detalle.subtotal
        carrito.save()
        
        if carrito.total == 0:
            mensaje += " Ha removido todos los productos del carrito..."

        linea_detalle.delete()

        producto_img = []
        allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

        for item in allProducts:
            
            imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

            producto_img.append({
                "img"         : imagen.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.precio, grouping=True),
                "cantidad"    : item.cantidad,
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                "id_carrito"  : item.id_carrito
            })
        
        contexto = {
                "title"           : "Carrito de Compras",
                "carrito_detalle" : producto_img,
                "mensaje"         : mensaje,
                "total"           : locale.format_string("%d", carrito.total, grouping=True),
                "id_carrito"      : carrito.id
        }

        return render(request, "CarritoApp/carrito_detalle.html", contexto)

    else:
        producto_img = []
        allProducts = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente).select_related('id_producto')

        for item in allProducts:
            
            imagen = ProductoImg.objects.filter(id_producto = item.id_producto).first()

            producto_img.append({
                "img"         : imagen.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.precio, grouping=True),
                "cantidad"    : item.cantidad,
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True),
                "id_carrito"  : item.id_carrito
            })
        
        contexto = {
                "title"           : "Carrito de Compras",
                "carrito_detalle" : producto_img,
                "mensaje"         : "Acción inválida!",
                "total"           : locale.format_string("%d", carrito.total, grouping=True),
                "id_carrito"      : carrito.id
        }

        return render(request, "CarritoApp/carrito_detalle.html", contexto)
        
@login_required
def pre_finalizar_pedido(request):
    usuario = request.user
    cliente = User.objects.filter(username=usuario).first()
    carrito = Carrito.objects.filter(cliente = cliente).first()
    detalle = CarritoDetalle.objects.filter(id_carrito = carrito.id, cliente = cliente)

    locale.setlocale(locale.LC_ALL, 'es_CL')

    if request.method == "POST":
        ciudad    = request.POST["ciudad"].title()
        direccion = request.POST["direccion"].title()
        contacto  = request.POST["contacto"]
        
        linea = 1

        new_compra = Compra(
            cliente   = cliente,
            total     = carrito.total,
            ciudad    = ciudad,
            direccion = direccion, 
            contacto  = contacto, 
            fecha     = timezone.now().date())
        new_compra.save()

        for item in detalle:
            new_detalle = CompraDetalle(
                id_compra   = new_compra,
                linea       = linea,
                # id_producto = item.id_producto,
                id_producto = get_object_or_404(Producto, id=item.id_producto.id),
                precio      = item.precio,
                cantidad    = item.cantidad,
                subtotal    = item.subtotal
            )
            new_detalle.save()
            linea += 1

        carrito.delete()
        detalle.delete()

        compra = Compra.objects.filter(id = new_compra.id, cliente=cliente).order_by('-fecha').first()
        compra_detalle = CompraDetalle.objects.filter(id_compra = compra.id).select_related('id_producto') # .values('linea','id_producto','precio','cantidad','subtotal')

        producto_img = []

        for item in compra_detalle:

            img = ProductoImg.objects.filter(id_producto = item.id_producto).first()
            producto_img.append({
                "imagen"      : img.imagen,
                "linea"       : item.linea,
                "id_producto" : item.id_producto,
                "precio"      : locale.format_string("%d", item.id_producto.precio, grouping=True),
                "cantidad"    : locale.format_string("%d", item.cantidad, grouping=True),
                "subtotal"    : locale.format_string("%d", item.subtotal, grouping=True)
            })

        contexto = {
            "title"   : "Compra Finalizada",
            "titulo"  : "¡Compra realizada exitosamente!",
            "total"   : locale.format_string("%d", new_compra.total, grouping=True),
            "usuario" : usuario,
            # "detalle" : compra_detalle,
            "detalle" : producto_img,
            "fecha"   : new_compra.fecha.strftime('%d/%m/%Y'),
            "mensaje" : "Recibirás un correo electrónico de confirmación con más detalles. Si tienes alguna pregunta, no dudes en contactarnos."
        }

        return render(request, "CarritoApp/finalizar.html", contexto)
    
    for item in detalle:
        item.precio = locale.format_string("%d", item.precio, grouping=True)
        item.subtotal = locale.format_string("%d", item.subtotal, grouping=True)
    
    contexto = {
        "title"           : "Confirmar Compra",
        "carrito_detalle" : detalle,
        "usuario"         : cliente.first_name,
        "total"           : locale.format_string("%d", carrito.total, grouping=True)
    }

    return render(request, "CarritoApp/pre_finalizar.html", contexto)
    

def imprime(descripcion, parametro):
    print()
    print()
    print(descripcion, parametro)
    print()
    print()
