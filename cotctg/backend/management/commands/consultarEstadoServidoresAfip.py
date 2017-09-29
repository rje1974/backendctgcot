'''
Created on 31 ago. 2017

@author: Hugo Chavero
'''
from django.core.management.base import BaseCommand
from pyafipws.wsctg import WSCTG
from backend.utils import obtener_afip_token


class Command(BaseCommand):
    help = 'Consulta el estado de los servidores AFIP'

    def handle(self, *args, **options):
        self.stdout.write('Conectando a WS AFIP')
        token = obtener_afip_token()
        wsctg = WSCTG()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        self.stdout.write('Consultado estado..')
        wsctg.Dummy()
        self.stdout.write('AppServerStatus: {}'.format(wsctg.AppServerStatus))
        self.stdout.write('DbServerStatus: {}'.format(wsctg.DbServerStatus))
        self.stdout.write('AuthServerStatus: {}'.format(wsctg.AuthServerStatus))
        self.stdout.write('Fin operacion.')