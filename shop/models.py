import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Producto(models.Model):
    MARCAS = [
        ("Games Workshop", "Games Workshop"),
        ("Corvus Belli", "Corvus Belli"),
        ("Warlord Games", "Warlord Games"),
        ("Vallejo", "Vallejo"),
        ("Army Painter", "Army Painter"),
        ("Citadel Colour", "Citadel Colour"),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField()
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
    STATUS_VALUES = [
        ("Pendiente", "Pendiente"),
        ("Pagada", "Pagada")
    ]
    id = models.CharField(primary_key=True, max_length=12, unique=True)
    detalles = models.ManyToManyField("Producto", through="VentaProducto", related_name="ventas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=500)
    tipo = models.CharField(max_length=500)
    estado = models.CharField(max_length=500)
    codigo_postal = models.CharField(max_length=10)
    correo = models.CharField(max_length=500)
    telefono = models.CharField(max_length=50)
    fecha_venta = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS_VALUES, default="JR")

    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):

        if not self.id:
            # Custom id
            self.id = uuid.uuid4().hex[:12]
            while Venta.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4().hex[:12]
        super(Venta, self).save(*args, **kwargs)

    
    def get_sale_data_dict(self) -> dict:
        """ Return sale summary data as dictionary

        Returns:
            dict: Sale summary data
        """

        sale_data = {
            "Order Number": self.id,
            "Email": self.usuario.email,
            "Full Name": self.usuario.first_name +" " +self.usuario.last_name,
            "Address": self.direccion,
            "Total": self.total
        }

        return sale_data

    class Meta:
        verbose_name_plural = "Ventas"
        verbose_name = "Venta"

class VentaProducto(models.Model):
    venta = models.ForeignKey("Venta", on_delete=models.CASCADE, related_name="detalle_venta")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField()
    descripcion = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    fecha_publicacion = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='blogs')  # Aquí se establece la relación

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Blogs"
        verbose_name = "Blog"
