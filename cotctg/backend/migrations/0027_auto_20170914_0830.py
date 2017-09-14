# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_auto_20170914_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cot',
            name='rentas_codigo_unidad_medida',
            field=models.IntegerField(choices=[(1, 'Kilogramos'), (2, 'Litros'), (3, 'Unidades'), (4, 'Metros Cuadrados'), (5, 'Metros'), (6, 'Metros Cubicos'), (7, 'Pares')], verbose_name='Codigo Unidad Medida'),
        ),
    ]
