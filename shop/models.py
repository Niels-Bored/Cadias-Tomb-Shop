from django.db import models

# Create your models here.
class Producto(models.Model):
    MARCAS = [
        ('Corvus Belli', 'Corvus Belli'),
        ('Games Workshop', 'Games Workshop'),
        ('Warlord Games', 'Warlord Games'),
        ('Vallejo', 'Vallejo'),
        ('Army Painter', 'Army Painter')
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    url_imagen = models.CharField(max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100, choices=MARCAS, default='JR')
    stock = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Producto"


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Usuarios"
        verbose_name = "Usuario"


class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_venta = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

