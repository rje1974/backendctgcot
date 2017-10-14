'''
Created on 12 oct. 2017

@author: Hugo Chavero
'''
from django.core.management.base import BaseCommand
from backend.models import Cosecha, Especie, Localidad
import json
import os


class Command(BaseCommand):
    help = 'Exporta todas las Cosechas, Especies y Localidades cargadas desde AFIP a correspondientes archivos JSON'

    def handle(self, *args, **options):
        _list = []
        base_dir = 'data/export/'
                
        for model in [Cosecha, Especie]:
            for obj in model.objects.all():
                _dict = {}
                _dict['code'] = obj.codigo
                _dict['searchStr'] = obj.descripcion
                _list.append(_dict)
                
            export_to = os.path.join(base_dir, '{}.json'.format(model.__name__.lower()))
            with open(export_to, 'w') as f:
                f.write(json.dumps(_list))
            self.stdout.write('{} exportado a {}'.format(model.__name__, export_to))
            _list = []
            
        for obj in Localidad.objects.all():
            _dict = {}
            _dict['code'] = obj.codigo
            _dict['searchStr'] = '{} - {}'.format(obj.nombre, obj.provincia)
            _list.append(_dict)
            
        export_to = os.path.join(base_dir, '{}.json'.format(Localidad.__name__.lower()))
        with open(export_to, 'w') as f:
            f.write(json.dumps(_list))
            
        self.stdout.write('{} exportado a {}'.format(Localidad.__name__, export_to))