# Generated by Django 5.1.2 on 2024-10-27 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_auto_20241020_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarritoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
    ]
