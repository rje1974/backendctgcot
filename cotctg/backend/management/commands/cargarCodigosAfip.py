'''
Created on 31 ago. 2017

@author: root
'''
from django.core.management.base import BaseCommand
from backend.constants import CUIT_SOLICITANTE, ARBA_PROVINCIAS
from backend.models import Cosecha, Especie, Establecimiento, Provincia,\
    Localidad
from backend.utils import obtener_afip_token
from backend.clients import get_wsctg_client


class Command(BaseCommand):
    help = 'Carga toda la informacion correspondiente a Codigos de Localidades, Provincias, Cosechas, Especies, etc'

    PROVINCIAS_ARBA = {
        '24': 'V',
        '23': 'Z',
        '22': 'R',
        '21': 'L',
        '20': 'Q',
        '19': 'N',
        '18': 'P',
        '17': 'U',
        '16': 'H',
        '14': 'T',
        '13': 'G',
        '12': 'S',
        '11': 'D',
        '10': 'J',
        '9': 'A',
        '8': 'F',
        '7': 'M',
        '6': 'Y',
        '5': 'E',
        '4': 'W',
        '3': 'X',
        '2': 'K',
        '1': 'B',
        '0': 'C'
        }
        

    def handle(self, *args, **options):
        self.stdout.write('Conectando a WS AFIP')
        token = obtener_afip_token()
        wsctg = get_wsctg_client()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        wsctg.Cuit = CUIT_SOLICITANTE
        sep = ','
        self.stdout.write('Borrando datos pre existentes')
        Cosecha.objects.all().delete()
        Especie.objects.all().delete()
        Establecimiento.objects.all().delete()
        Localidad.objects.all().delete()
        Provincia.objects.all().delete()
        
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

        self.stdout.write('Cargando Provincias y Localidades')
        # Carga de Provincias y Localidades
        provincias = wsctg.ConsultarProvincias(sep=sep)
        for provincia in provincias:
            provincia = provincia.split(sep)
            codigo = provincia[1].strip()
            nombre = provincia[2].strip()
            codigo_arba = self.PROVINCIAS_ARBA[codigo]
            print "Codigo afip: {}, codigo arba: {}, nombre: {}".format(codigo, codigo_arba, nombre)
            obj_provincia = Provincia.objects.create(codigo=codigo, 
                                                     nombre=nombre,
                                                     codigo_arba=codigo_arba)
            localidades = wsctg.ConsultarLocalidadesPorProvincia(codigo_provincia=codigo, sep=sep)
            for localidad in localidades:
                localidad = localidad.split(sep)
                codigo = localidad[1].strip()
                nombre = localidad[2].strip()
                Localidad.objects.create(provincia=obj_provincia, codigo=codigo, nombre=nombre)
        self.stdout.write('Datos Importados con Exito')