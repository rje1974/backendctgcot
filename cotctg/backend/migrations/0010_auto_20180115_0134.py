# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-15 04:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20171029_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='provincia',
            name='codigo_arba',
            field=models.CharField(default='', max_length=30, verbose_name='Codigo ARBA'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credencial',
            name='cuit_solicitante',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999999999)], verbose_name='CUIT Solicitante'),
        ),
        migrations.AlterField(
            model_name='credencial',
            name='pass_arba',
            field=models.CharField(blank=True, max_length=30, verbose_name='Contrasena ARBA'),
        ),
        migrations.AlterField(
            model_name='credencial',
            name='usuario_arba',
            field=models.CharField(blank=True, max_length=12, verbose_name='Usuario ARBA'),
        ),
    ]
