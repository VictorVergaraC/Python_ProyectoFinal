from django.db import models

class Carrito(models.Model):
    cliente = models.IntegerField()
    total   = models.IntegerField()


    pass

class CarritoDetalle(models.Model):
    cliente  = models.IntegerField()
    linea    = models.IntegerField()
    producto = models.IntegerField()
    cantidad = models.IntegerField()

    pass
