from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)
    activa      = models.BooleanField()

    def __str__(self):
        return f"Categoría: {self.descripcion}"

class Producto(models.Model):
    descripcion   = models.CharField(max_length=100)
    categoria     = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    precio        = models.IntegerField()
    oferta        = models.BooleanField()
    precio_oferta = models.IntegerField()
    activo        = models.BooleanField()

    def __str__(self):
        return f"Producto: {self.descripcion}"

    
class ProductoImg(models.Model):
    imagen      = models.ImageField(upload_to="products")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Producto: {self.id_producto.descripcion}"
    
    
class ComentarioProducto(models.Model):
    descripcion = models.CharField(max_length=100)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cliente     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha       = models.DateField()
    
    def __str__(self):
        return f"{self.cliente.first_name} ({self.fecha.strftime('%d/%m/%Y')}) acerca de '{self.producto.descripcion}' dice: {self.descripcion}"
