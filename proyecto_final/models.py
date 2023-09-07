from django.db import models
from django.contrib.auth.models import User
from ProductosApp.models import Producto

class Compra(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    total   = models.IntegerField()
    
class CompraDetalle(models.Model):
    id_compra   = models.ForeignKey(Compra, on_delete=models.CASCADE, null=False, blank=False)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False, blank=False)
    precio      = models.IntegerField()
    cantidad    = models.IntegerField()
    subtotal    = models.IntegerField()