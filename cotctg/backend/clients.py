'''
Created on 5 oct. 2017

@author: Hugo Chavero
'''
from pyafipws import wsctg, wsaa
from pyafipws.cot import COT
from cotctg.settings import AFIP_CLIENT_DEBUG
from backend.constants import HOMO, WSCTG_WSDL, WSAA_URL


def get_wsctg_client():
        wsctg.HOMO = HOMO
        wsctg.WSDL = WSCTG_WSDL
        wsctg.DEBUG = AFIP_CLIENT_DEBUG
        return wsctg.WSCTG()


def get_wsaa_client():        
    wsaa.HOMO = HOMO
    wsaa.WSDL = WSCTG_WSDL
    wsaa.DEBUG = AFIP_CLIENT_DEBUG
    wsaa.WSAAURL = WSAA_URL
    return wsaa.WSAA()


def get_wscot_client(usuario, contrasena):
    cot = COT()
    cot.Usuario = usuario
    cot.Password = contrasena
    return cot