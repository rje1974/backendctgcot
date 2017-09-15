# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 16:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_auto_20170914_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cot',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Operacion'),
        ),
        migrations.AlterField(
            model_name='ctg',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now, null=True, verbose_name='Fecha de Operacion'),
        ),
    ]
