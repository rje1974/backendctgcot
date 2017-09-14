# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 19:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20170912_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctg',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre de CTG'),
        ),
        migrations.AlterField(
            model_name='ctg',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(1, 'Parcial'), (2, 'Generado'), (3, 'Anulado'), (4, 'Arribado')], default=1, null=True, verbose_name='Estado del CTG'),
        ),
        migrations.AlterField(
            model_name='ctg',
            name='operacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ctg', to='backend.Operacion'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='tipo_operacion',
            field=models.CharField(choices=[(1, 'CTG Solicitado'), (2, 'CTG carga parcial'), (3, 'CTG Anulado'), (4, 'COT')], max_length=20, verbose_name='Tipo de Operacion'),
        ),
    ]