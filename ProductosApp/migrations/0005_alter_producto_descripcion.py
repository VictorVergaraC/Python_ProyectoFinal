# Generated by Django 4.0 on 2023-09-08 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductosApp', '0004_rename_descripicion_producto_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(max_length=100),
        ),
    ]
