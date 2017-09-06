# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 15:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20170906_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidad',
            name='usuario_solicitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Solicitante'),
        ),
    ]
