'''
Created on 31 ago. 2017

@author: Hugo Chavero
'''
from django.core.management.base import BaseCommand
from backend.utils import obtener_afip_token
from backend.clients import get_wsctg_client


class Command(BaseCommand):
    help = 'Consulta el estado de los servidores AFIP'

    def handle(self, *args, **options):
        self.stdout.write('Conectando a WS AFIP')
        token = obtener_afip_token()
        wsctg = get_wsctg_client()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        self.stdout.write('Consultado estado..')
        wsctg.Dummy()
        self.stdout.write('AppServerStatus: {}'.format(wsctg.AppServerStatus))
        self.stdout.write('DbServerStatus: {}'.format(wsctg.DbServerStatus))
        self.stdout.write('AuthServerStatus: {}'.format(wsctg.AuthServerStatus))
        self.stdout.write('Fin operacion.')