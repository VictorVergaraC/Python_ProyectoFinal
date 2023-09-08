from django.db import models

from django.db import models
from django.contrib.auth.models import User
from ProductosApp.models import Producto

class Compra(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total   = models.IntegerField()
    fecha   = models.DateField()
    
class CompraDetalle(models.Model):
    id_compra   = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    precio      = models.IntegerField()
    cantidad    = models.IntegerField()
    subtotal    = models.IntegerField()
