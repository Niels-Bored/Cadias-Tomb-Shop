# Generated by Django 4.2.7 on 2025-04-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_alter_blog_url_imagen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="url_imagen",
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name="producto",
            name="url_imagen",
            field=models.URLField(),
        ),
    ]
