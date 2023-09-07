from django.db import models
from django.contrib.auth.models import User
from ProductosApp.models import Producto

class Carrito(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total   = models.IntegerField()


class CarritoDetalle(models.Model):
    id_carrito  = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True, blank=True)
    cliente     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    linea       = models.IntegerField(default=1)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    precio      = models.IntegerField(default=0)
    cantidad    = models.IntegerField(default=1)
    subtotal    = models.IntegerField(default=0)

    pass
