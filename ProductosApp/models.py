from django.db import models

class Producto(models.Model):
    descrpicion   = models.CharField(max_length=50)
    categoria     = models.CharField(max_length=50)
    precio        = models.IntegerField()
    oferta        = models.BooleanField()
    precio_oferta = models.IntegerField()
    activo        = models.BooleanField()

    def __str__(self):
        return f"Producto: {self.nombre}"

class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)
    activa      = models.BooleanField()

    def __str__(self):
        return f"Producto: {self.descripcion}"
