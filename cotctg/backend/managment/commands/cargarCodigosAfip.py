'''
Created on 31 ago. 2017

@author: root
'''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pyafipws.wsctg import WSCTG
from cotctg.backend.constants import CUIT_SOLICITANTE
from cotctg.backend.models import Cosecha, Especie, Establecimiento, Provincia,\
    Localidad


class Command(BaseCommand):
    help = 'Carga toda la informacion correspondiente a Codigos de Localidades, Provincias, Cosechas, Especies, etc'

    def handle(self, *args, **options):
        self.stdout.write('Conectando a WS AFIP')
        usuario = User.objects.get(is_superuser=True)
        token = usuario.credenciales.obtener_afip_token()
        wsctg = WSCTG()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        wsctg.Cuit = CUIT_SOLICITANTE
        sep = ','
        
        self.stdout.write('Cargando cosechas')
        # Carga de Cosechas
        cosechas = wsctg.ConsultarCosechas(sep=sep)
        for cosecha in cosechas:
            cosecha = cosecha.split(sep)
            codigo = cosecha[1].strip()
            descripcion = cosecha[2].strip()
            Cosecha.objects.create(codigo=codigo, descripcion=descripcion)

        self.stdout.write('Cargando Especies')
        # Carga de Especies
        especies = wsctg.ConsultarEspecies(sep=sep)
        for especie in especies:
            especie = especie.split(sep)
            codigo = especie[1].strip()
            descripcion = especie[2].strip()
            Especie.objects.create(codigo=codigo, descripcion=descripcion)

        self.stdout.write('Cargando Establecimientos')
        # Carga de Establecimientos
        establecimientos = wsctg.ConsultarEstablecimientos(sep=sep)
        for establecimiento in establecimientos:
            establecimiento = establecimiento.split(sep)
            codigo = establecimiento[1].strip()
            descripcion = establecimiento[2].strip()
            Establecimiento.objects.create(codigo=codigo, descripcion=descripcion)

        self.stdout.write('Cargando Provincias')
        # Carga de Provincias y Localidades
        provincias = wsctg.ConsultarProvincias(sep=sep)
        for provincia in provincias:
            provincia = provincia.split(sep)
            codigo = provincia[1].strip()
            nombre = provincia[2].strip()
            Provincia.objects.create(codigo=codigo, nombre=nombre)
            localidades = wsctg.ConsultarLocalidadesPorProvincia(codigo_provincia=codigo, sep=sep)
            for localidad in localidades:
                localidad = localidad.split(sep)
                codigo = localidad[1].strip()
                nombre = localidad[2].strip()
                Localidad.objects.create(provincia=provincia, codigo=codigo, nombre=nombre)
        self.stdout.write('Datos Importados con Exito')