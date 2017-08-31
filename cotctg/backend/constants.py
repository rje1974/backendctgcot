
# Constantes WebService AFIP

AFIP_DEBUG = True
CUIT_SOLICITANTE = 20244416722
CACERT = 'afip_ca_info.crt'


if AFIP_DEBUG:
    # AFIP Homologacion (ambiente de pruebas)
    WSCTG_WSDL = "https://fwshomo.afip.gov.ar/wsctg/services/CTGService_v4.0?wsdl"
    WSAA_WSDL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    WSAA_URL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
    DEBUG = True
    HOMO = True
else:
    # AFIP Produccion
    WSCTG_WSDL = "https://serviciosjava.afip.gob.ar/wsctg/services/CTGService_v4.0?wsdl"
    WSAA_WSDL = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"
    WSAA_URL = "https://wsaa.afip.gov.ar/ws/services/LoginCms"
    DEBUG = False
    HOMO = False
