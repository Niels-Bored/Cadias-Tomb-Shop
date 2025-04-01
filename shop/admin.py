from django.contrib import admin
from shop import models

# Register your models here.
@admin.register(models.Producto)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'marca', 'stock')
    search_fields = ('nombre','marca')
    list_filter = ('marca',)

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido_p', 'apellido_m', 'correo')
    earch_fields = ('nombre','apellido_p', 'apellido_m', 'correo')