# Generated by Django 4.0 on 2023-09-01 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductosApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='products')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ProductosApp.producto')),
            ],
        ),
    ]
