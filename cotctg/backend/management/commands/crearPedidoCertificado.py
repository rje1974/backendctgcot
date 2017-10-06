'''
Created on 6 oct. 2017

@author: Hugo Chavero
'''
from django.core.management.base import BaseCommand
from backend.clients import get_wsaa_client

class Command(BaseCommand):
    help = 'Crea archivos key y csr'

    def handle(self, *args, **options):
        wsaa = get_wsaa_client()
        self.stdout.write('Creando Clave Privada')
        res = wsaa.CrearClavePrivada('ctgapp.key')
        self.stdout.write('resultado: {}'.format(res))
        self.stdout.write('Creando Pedido de Certificado')
        res = wsaa.CrearPedidoCertificado(cuit='20244416722', empresa='RIVA JUAN EDUARDO', nombre='ctgapp', filename='ctgapp.csr')
        self.stdout.write('resultado: {}'.format(res))
        self.stdout.write('Fin')