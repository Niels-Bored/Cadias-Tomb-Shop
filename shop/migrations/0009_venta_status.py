# Generated by Django 4.2.7 on 2025-04-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_venta_codigo_postal_venta_correo_venta_estado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="venta",
            name="status",
            field=models.CharField(
                choices=[("Pendiente", "Pendiente"), ("Pagada", "Pagada")],
                default="JR",
                max_length=100,
            ),
        ),
    ]
