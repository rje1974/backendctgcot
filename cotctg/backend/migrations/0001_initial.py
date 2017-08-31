# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 14:54
from __future__ import unicode_literals

import backend.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cosecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Cosecha',
                'verbose_name_plural': 'Cosechas',
            },
        ),
        migrations.CreateModel(
            name='Credencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.FileField(upload_to=backend.models.user_directory_path, verbose_name='Clave Privada')),
                ('certificado', models.FileField(upload_to=backend.models.user_directory_path, verbose_name='Certificado')),
                ('certificado_texto', models.TextField(blank=True, verbose_name='Text de Certificado')),
                ('wsaa_token', models.FileField(blank=True, upload_to=b'', verbose_name='Token WSAA (TA)')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credenciales', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Credenciales AFIP',
                'verbose_name_plural': 'Credenciales AFIP',
            },
        ),
        migrations.CreateModel(
            name='CTG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_carta_de_porte', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999999999)], verbose_name='Nro Carta de Porte')),
                ('remitente_comercial_como_canjeador', models.BooleanField(default=False, verbose_name='Rte Comercial actua como Canjeador?')),
                ('remitente_comercial_como_productor', models.BooleanField(default=False, verbose_name='Rte Comercial actua como Productor?')),
                ('codigo_localidad_origen', models.PositiveIntegerField(verbose_name='Codigo Localidad Origen')),
                ('codigo_localidad_destino', models.PositiveIntegerField(verbose_name='Codigo Localidad Destino')),
                ('codigo_cosecha', models.PositiveIntegerField(verbose_name='Codigo Cosecha')),
                ('peso_neto_carga', models.PositiveIntegerField(verbose_name='Peso Neto de Carga')),
                ('cant_horas', models.PositiveIntegerField(blank=True, verbose_name='Cantidad de Horas')),
                ('patente_vehiculo', models.CharField(blank=True, max_length=30, verbose_name='Patente Vehiculo')),
                ('km_a_recorrer', models.PositiveIntegerField(blank=True, verbose_name='Km a Recorrer')),
                ('turno', models.CharField(blank=True, max_length=50, verbose_name='Turno')),
                ('estado', models.IntegerField(choices=[(1, 'Sin Generar'), (2, 'Generado'), (3, 'Datos Pendientes'), (4, 'Anulado'), (5, 'Arribado')], default=1, verbose_name='Estado del CTG')),
                ('geolocalizacion', models.CharField(blank=True, max_length=150, verbose_name='Geo Localizacion de la Solicitud')),
                ('numero_ctg', models.CharField(blank=True, max_length=50, verbose_name='Nro CTG')),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True, verbose_name='Observaciones')),
                ('fechahora', models.CharField(blank=True, max_length=200, null=True, verbose_name='Fecha y Hora')),
                ('vigenciadesde', models.CharField(blank=True, max_length=200, null=True, verbose_name='Vigencia Desde')),
                ('vigenciahasta', models.CharField(blank=True, max_length=200, null=True, verbose_name='Vigencia Hasta')),
                ('tarifareferencia', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tarifa Referencia')),
                ('errores', models.CharField(blank=True, max_length=200, null=True, verbose_name='Errores')),
                ('controles', models.CharField(blank=True, max_length=200, null=True, verbose_name='Controles')),
            ],
            options={
                'verbose_name': 'CTG',
                'verbose_name_plural': 'CTGs',
            },
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre de Entidad')),
                ('cuit', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999999999)], verbose_name='CUIT')),
                ('actua_como', models.IntegerField(choices=[(1, 'Remitente Comercial'), (2, 'Destino'), (3, 'Destinatario'), (4, 'Corredor'), (5, 'Transportista')], verbose_name='Act\xfaa como')),
                ('usuario_solicitante', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Usuario Solicitante')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Especie',
                'verbose_name_plural': 'Especies',
            },
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Establecimiento',
                'verbose_name_plural': 'Establecimientos',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo')),
                ('nombre', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Localidad',
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Operacion')),
                ('tipo_operacion', models.CharField(choices=[(1, 'Solicitud CTG desde Inicio'), (2, 'Solicitud CTG dato Pendiente'), (3, 'Anular CTG')], max_length=20, verbose_name='Tipo de Operacion')),
                ('ctg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.CTG')),
            ],
            options={
                'verbose_name': 'Operacion',
                'verbose_name_plural': 'Operaciones',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(verbose_name='Codigo')),
                ('nombre', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Provincia'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='cuit_corredor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ctg_corredor', to='backend.Entidad', verbose_name='Cuit Corredor'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='cuit_destinatario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ctg_destinatario', to='backend.Entidad', verbose_name='Cuit Destinatario'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='cuit_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ctg_destino', to='backend.Entidad', verbose_name='Cuit Destino'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='cuit_remitente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ctg_remitente', to='backend.Entidad', verbose_name='Cuit Remitente Comercial'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='cuit_transportista',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ctg_transportista', to='backend.Entidad', verbose_name='Cuit Tranportista'),
        ),
        migrations.AddField(
            model_name='ctg',
            name='usuario_solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Solicitante'),
        ),
    ]
