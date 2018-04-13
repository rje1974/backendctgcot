from cotctg.settings import AFIP_HOMO

# Constantes WebService AFIP

CUIT_SOLICITANTE = 20244416722
# CUIT_SOLICITANTE = 30552651282
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
# ESTADOS CTG
CTG_ESTADO_PENDIENTE = 1
CTG_ESTADO_GENERADO = 2
CTG_ESTADO_ANULADO = 3
CTG_ESTADO_ARRIBADO = 4
CTG_ESTADO_ERROR = 5

# ESTADOS COT
COT_ESTADO_PENDIENTE = 1
COT_ESTADO_GENERADO = 2
COT_ESTADO_ERROR = 3

# ACCIONES CTG
CTG_ACCION_PARCIAL = 1
CTG_ACCION_SOLICITAR = 2

# ACCIONES COT
COT_ACCION_SOLICTAR = 1

# Tablas ARBA

ARBA_MEDIDAS = (
    (1, 'Kilogramos'),
    (2, 'Litros'),
    (3, 'Unidades'),
    (4, 'Metros Cuadrados'),
    (5, 'Metros'),
    (6, 'Metros Cubicos'),
    (7, 'Pares'),
)

ARBA_PROVINCIAS = (
    ('A', 'Salta'),
    ('B', 'Buenos Aires'),
    ('C', 'Capital Federal'),
    ('D', 'San Luis'),
    ('E', 'Entre Rios'),
    ('F', 'La Rioja'),
    ('G', 'Santiago del Estero'),
    ('H', 'Chaco'),
    ('J', 'San Juan'),
    ('K', 'Catamarca'),
    ('L', 'La Pampa'),
    ('M', 'Mendoza'),
    ('N', 'Misiones'),
    ('P', 'Formosa'),
    ('Q', 'Neuquen'),
    ('R', 'Rio Negro'),
    ('S', 'Santa Fe'),
    ('T', 'Tucuman'),
    ('U', 'Chubut'),
    ('V', 'T.N.T. del Fuego'),
    ('W', 'Corrientes'),
    ('X', 'Cordoba'),
    ('Y', 'Jujuy'),
    ('Z', 'Santa Cruz'),
    )

ARBA_COMPROBANTES = (
    ('74 P', 'Carta de Porte'),
    ('91 R', 'Remito R'),
    ('01 A', 'Factura A'),
    ('60 A', 'Cuenta de Venta y Liquido Producto A'),
    ('94 X', 'Remito X'),
    ('06 B', 'Factura B'),
    ('92 C', 'Factura C'),
    ('51 M', 'Factura M'),
    ('61 B', 'Cuenta de Venta y Liquido Producto B'),
    ('93 C', 'Cuenta de Venta y Liquido Producto C'),
    ('58 M', 'Cuenta de Venta y Liquido Producto M'),
    ('95 G', 'Guia Unica de Traslado'),
    ('97 E', 'Documento Equivalente'),
    )
