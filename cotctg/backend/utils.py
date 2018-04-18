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


def validar_cuit(cuit):
    cuit = str(cuit)
    # validaciones minimas
    if len(cuit) != 11:
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    cuit = cuit.replace("-", "").replace("/", "") # remuevo las barras

    # Calculo el digito verificador:
    aux = 0
    for i in xrange(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])