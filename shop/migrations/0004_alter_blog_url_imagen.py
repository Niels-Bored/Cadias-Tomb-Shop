# Generated by Django 4.2.7 on 2025-04-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_blog_descripcion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="url_imagen",
            field=models.URLField(max_length=300),
        ),
    ]
