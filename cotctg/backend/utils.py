'''
Created on 29 sep. 2017

@author: Hugo Chavero
'''

from backend.constants import WSAA_WSDL, CACERT
from cotctg.settings import AFIP_CERT, AFIP_KEY
from backend.clients import get_wsaa_client
import datetime


def obtener_afip_token():
    wsaa = get_wsaa_client()
    wsaa_token = wsaa.Autenticar("wsctg", AFIP_CERT, AFIP_KEY, wsdl=WSAA_WSDL, cacert=CACERT)
    return wsaa_token


def obtener_fecha_frontend(obj):
    fecha = datetime.datetime.strptime(obj.fecha_salida_transporte, "%Y%m%d")
    return fecha.strftime("%d-%m-%Y")
