from django.db import models

class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)
    activa      = models.BooleanField()

    def __str__(self):
        return f"Categoría: {self.descripcion}"

class Producto(models.Model):
    descripcion   = models.CharField(max_length=100)
    # categoria     = models.CharField(max_length=50)
    categoria     = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    precio        = models.IntegerField()
    oferta        = models.BooleanField()
    precio_oferta = models.IntegerField()
    activo        = models.BooleanField()

    def __str__(self):
        return f"Producto: {self.descripcion}"

    
class ProductoImg(models.Model):
    imagen   = models.ImageField(upload_to="products")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Producto: {self.producto}"
