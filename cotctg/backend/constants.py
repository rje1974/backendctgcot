from cotctg.settings import AFIP_HOMO

# Constantes WebService AFIP


CUIT_SOLICITANTE = 20244416722
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

COT_ESTADO_PENDIENTE = 1
COT_ESTADO_GENERADO = 2

CTG_ACCION_PARCIAL = 1
CTG_ACCION_SOLICITAR = 2

COT_ACCION_SOLICTAR = 1