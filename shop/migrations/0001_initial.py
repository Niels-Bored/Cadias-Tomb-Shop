# Generated by Django 4.2.7 on 2025-03-31 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('url_imagen', models.CharField(max_length=300)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marca', models.CharField(choices=[('Corvus Belli', 'Corvus Belli'), ('Games Workshop', 'Games Workshop'), ('Warlord Games', 'Warlord Games'), ('Vallejo', 'Vallejo'), ('Army Painter', 'Army Painter')], default='JR', max_length=100)),
                ('stock', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_p', models.CharField(max_length=100)),
                ('apellido_m', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('contraseña', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.usuario')),
            ],
        ),
    ]
