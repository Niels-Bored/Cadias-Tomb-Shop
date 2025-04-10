from django.contrib import admin
from shop import models

# Register your models here.
@admin.register(models.Producto)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'marca', 'stock')
    search_fields = ('nombre','marca')
    list_filter = ('marca',)

@admin.register(models.Venta)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('producto', 'usuario', 'direccion', 'fecha_venta', 'total')
    search_fields = ('usuario',)

@admin.register(models.Blog)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'autor', 'fecha_publicacion')
    search_fields = ('titulo','autor')