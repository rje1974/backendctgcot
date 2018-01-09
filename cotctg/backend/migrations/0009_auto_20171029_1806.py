# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 21:06
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0008_auto_20171019_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credencial',
            name='usuario',
        ),
        migrations.AddField(
            model_name='credencial',
            name='credenciales_produccion',
            field=models.BooleanField(default=True, verbose_name='Credenciales en Produccion'),
        ),
        migrations.AddField(
            model_name='credencial',
            name='cuit_solicitante',
            field=models.BigIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(99999999999)], verbose_name='CUIT Solicitante'),
        ),
        migrations.AddField(
            model_name='credencial',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credenciales', to=settings.AUTH_USER_MODEL),
        ),
    ]
