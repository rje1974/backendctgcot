# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20170831_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctg',
            name='numero_carta_de_porte',
            field=models.CharField(max_length=12, verbose_name='Nro Carta de Porte'),
        ),
    ]
