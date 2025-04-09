from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Producto(models.Model):
    MARCAS = [
        ("Corvus Belli", "Corvus Belli"),
        ("Games Workshop", "Games Workshop"),
        ("Warlord Games", "Warlord Games"),
        ("Vallejo", "Vallejo"),
        ("Army Painter", "Army Painter"),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    url_imagen = models.URLField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100, choices=MARCAS, default="JR")
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Producto"

    def reduce_stock(self, amount: int) -> bool:
        """Method to reduce amount from stock product

        Args:
            amount (int): Amount of products to reduce from stock
        
        Returns:
            bool: True if amount can be reduced without exceeding stock, False in case it can't

        """
        if self.stock >= amount:
            self.stock -= amount
            return True
        else:
            return False

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=500)
    fecha_venta = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "Ventas"
        verbose_name = "Venta"


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    url_imagen = models.URLField()
    descripcion = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    fecha_publicacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Blogs"
        verbose_name = "Blog"
