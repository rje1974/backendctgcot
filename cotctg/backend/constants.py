from cotctg.settings import AFIP_HOMO

# Constantes WebService AFIP

CUIT_SOLICITANTE = 20244416722
#CUIT_SOLICITANTE = 30552651282
'''
TODO:
Al ingresar otro CUIT Solicitante que no sea 20244416722, recibo el mensaje:
 
La CUIT del usuario representante 20244416722 no corresponde a una CUIT habilitada por el Administrador de Relaciones de la AFIP para el Contribuyente 30552651282.

'''


CACERT = 'afip_ca_info.crt'


if AFIP_HOMO:
    # AFIP Homologacion (ambiente de pruebas)
    WSCTG_WSDL = "https://fwshomo.afip.gov.ar/wsctg/services/CTGService_v4.0?wsdl"
    WSAA_WSDL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    WSAA_URL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
    HOMO = AFIP_HOMO
else:
    # AFIP Produccion
    WSCTG_WSDL = "https://serviciosjava.afip.gob.ar/wsctg/services/CTGService_v4.0?wsdl"
    WSAA_WSDL = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"
    WSAA_URL = "https://wsaa.afip.gov.ar/ws/services/LoginCms"
    HOMO = AFIP_HOMO



# Constantes de modelos de ddtos

CTG_ESTADO_PENDIENTE = 1
CTG_ESTADO_GENERADO = 2
CTG_ESTADO_ANULADO = 3
CTG_ESTADO_ARRIBADO = 4
CTG_ESTADO_ERROR = 5

COT_ESTADO_PENDIENTE = 1
COT_ESTADO_GENERADO = 2
COT_ESTADO_ERROR = 3

CTG_ACCION_PARCIAL = 1
CTG_ACCION_SOLICITAR = 2

COT_ACCION_SOLICTAR = 1
