'''
Created on 29 sep. 2017

@author: Hugo Chavero
'''

from pyafipws.wsaa import WSAA
from backend.constants import HOMO, DEBUG, WSAA_URL, WSAA_WSDL, CACERT
from cotctg.settings import AFIP_CERT, AFIP_KEY


def obtener_afip_token():
    wsaa = WSAA()
    wsaa.HOMO = HOMO
    wsaa.DEBUG = DEBUG
    wsaa.WSAAURL = WSAA_URL
    wsaa_token = wsaa.Autenticar("wsctg", AFIP_CERT, AFIP_KEY, wsdl=WSAA_WSDL, debug=DEBUG, cacert=CACERT)
    return wsaa_token