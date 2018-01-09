'''
Created on 12 oct. 2017

@author: Hugo Chavero
'''
from django.core.management.base import BaseCommand
from backend.models import Cosecha, Especie, Localidad, Provincia
import json
import os

EXPORT_DIR = 'data/export/'


class Command(BaseCommand):
    help = 'Exporta todas las Cosechas, Especies, Provincias y Localidades por \
    provincias cargadas desde AFIP a correspondientes archivos JSON'

    def handle(self, *args, **options):
        self.stdout.write('Inicio de Exports a dir: {}'.format(EXPORT_DIR))

        source_list = []
        for model in [Cosecha, Especie]:
            for obj in model.objects.all():
                _dict = {}
                _dict['code'] = obj.codigo
                _dict['searchStr'] = obj.descripcion
                source_list.append(_dict)
                
            self._export_query(model.__name__, source_list)    
            source_list = []
        
        prov_list=[]
        for provincia in Provincia.objects.all():
            _dict['code'] = provincia.codigo
            _dict['searchStr'] = provincia.nombre
            prov_list.append(_dict)
            
            loc_list=[]
            for obj in Localidad.objects.filter(provincia=provincia):
                _dict = {}
                _dict['code'] = obj.codigo
                _dict['searchStr'] = obj.nombre
                loc_list.append(_dict)
            self._export_query(str(provincia.codigo), loc_list)
        self._export_query(Provincia.__name__, prov_list)
            
    def _export_query(self, file_name, source_list):
        export_to = os.path.join(EXPORT_DIR, '{}.json'.format(file_name.lower()))
        with open(export_to, 'w') as f:
                f.write(json.dumps(source_list))
        self.stdout.write('{} exportado.'.format(file_name))