# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_auto_20170914_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctg',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.localdate, null=True, verbose_name='Fecha de Operacion'),
        ),
    ]
