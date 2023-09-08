from django.db import models

from django.db import models
from django.contrib.auth.models import User
from ProductosApp.models import Producto

class Compra(models.Model):
    cliente   = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total     = models.IntegerField()
    ciudad    = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=150, null=True)
    contacto  = models.IntegerField()
    fecha     = models.DateField()

    def __str__(self):
        nombre_cliente = self.cliente.username if self.cliente else "Cliente Desconocido"

        fecha_formateada = self.fecha.strftime('%d/%m/%Y')

        return f"Nombre del Cliente: {nombre_cliente}, Total: {self.total}, Fecha: {fecha_formateada}"

    
class CompraDetalle(models.Model):
    id_compra   = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    precio      = models.IntegerField()
    cantidad    = models.IntegerField()
    subtotal    = models.IntegerField()

    def __str__(self):
        descripcion_producto = self.id_producto.descripcion if self.id_producto else "Producto Desconocido"

        return f"ID Producto: {self.id_producto.id}, Descripción: {descripcion_producto}, Precio: {self.precio}, Cantidad: {self.cantidad}, Subtotal: {self.subtotal}"
