# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .constants import HOMO, CUIT_SOLICITANTE
from django.utils import timezone
from backend.constants import WSCTG_WSDL, CTG_ESTADO_GENERADO\
    , CTG_ESTADO_PENDIENTE, CTG_ESTADO_ANULADO,\
    CTG_ESTADO_ARRIBADO, CTG_ACCION_SOLICITAR, CTG_ACCION_PARCIAL,\
    COT_ESTADO_PENDIENTE, COT_ESTADO_GENERADO, CTG_ESTADO_ERROR, ARBA_MEDIDAS,\
    ARBA_COMPROBANTES, COT_ESTADO_ERROR
from backend.utils import obtener_afip_token
from backend.clients import get_wscot_client, get_wsctg_client
import json
from cotctg.settings import BASE_DIR
import os
from django.core.validators import MaxValueValidator


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.usuario.id, filename)


class Perfil(models.Model):
    '''
    Representa las credenciales de autenticacion del usuario ante AFIP y ARBA
    '''
    user = models.OneToOneField(User, related_name='credenciales')
    alias = models.CharField('Nombre y Apellido', max_length=150, blank=True)
    usuario_arba = models.CharField('Usuario ARBA', max_length=12, blank=True)
    pass_arba = models.CharField('Contrasena ARBA', max_length=30, blank=True)
    cuit_solicitante = models.BigIntegerField('CUIT Solicitante', validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    credenciales_produccion = models.BooleanField('Credenciales en Produccion', default=True)
    afip_habilitado = models.BooleanField('Servicios AFIP habilitados ?', default=False)
    
    def __unicode__(self):
        return "Credenciales de {}".format(self.user)
    
    class Meta:
        verbose_name = 'Credenciales'
        verbose_name_plural = 'Credenciales'


class Entidad(models.Model):
    ACTUA_COMO = ((1, 'Remitente Comercial'),
                (2, 'Destino'),
                (3, 'Destinatario'),
                (4, 'Corredor'),
                (5, 'Transportista'),)
    usuario_solicitante = models.ForeignKey(User, verbose_name='Usuario Solicitante', null=True)
    nombre = models.CharField('Nombre de Entidad', max_length=120)
    cuit = models.CharField('CUIT', max_length=11, primary_key=True)
    actua_como = models.IntegerField('Actúa como', choices=ACTUA_COMO, null=True, blank=True)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        
        
        
class COT(models.Model):
    '''
    Representa un Codigo de Operacion Traslado/Transporte
    (Por el momento se incluyen solo los campos requeridos)
    
    Campos que se agregan manualmente al txt:
    tipo_registro
    cantidad_total_remitos
    '''
    COT_ESTADO = (
        (COT_ESTADO_PENDIENTE, 'Parcial'),
        (COT_ESTADO_GENERADO, 'Generado'),
    )
    
    SUJETO_GENERADOR =(
            ('E', 'Emisor'),
            ('D', 'Destinatario')
        )
    SI_NO = (
            ('SI', 'Si'),
            ('NO', 'No')
        )

    ARBA_DATE_FORMAT = ('%Y%m%%d')
    
    usuario_solicitante = models.ForeignKey(User, verbose_name='Usuario Solicitante')
    cuit_empresa = models.CharField('CUIT Empresa', max_length=11)
    fecha_emision = models.CharField('Fecha Emision (AAAAMMDD)', max_length=8)
    tipo_comprobante = models.CharField('Tipo de Comprobante', max_length=4, choices=ARBA_COMPROBANTES)
    nro_comprobante = models.BigIntegerField('Nro Comprobante', validators=[MaxValueValidator(999999999999)])
    fecha_salida_transporte = models.CharField('Fecha Salida Transporte (AAAAMMDD)', max_length=8)
    sujeto_generador = models.CharField('Sujeto Generador', choices=SUJETO_GENERADOR, max_length=1)
    destinatario_consumidor_final = models.BooleanField('Destinatario Consumidor Final?')
    destinatario_tenedor = models.BooleanField('Destinatario es Tenedor')
    destinatario_razon_social = models.CharField('Destinatario Razon Social', max_length=50, blank=True, null=True)
    destinatario_cuit = models.BigIntegerField('Destinatario Cuit', validators=[MaxValueValidator(99999999999)], blank=True, null=True)
    destino_domicilio_calle = models.CharField('Destino: Calle de Domicilio', max_length=40)
    destino_domicilio_codigopostal = models.CharField('Destino: Codigo Postal', max_length=8)
    destino_domicilio_localidad = models.ForeignKey('Localidad', verbose_name='Localidad de Destino', related_name='cot_localidad_destino')
    destino_domicilio_provincia = models.ForeignKey('Provincia', verbose_name='Provincia de Destino', related_name='cot_provincia_destino', to_field='codigo_arba')
    entrega_domicilio_origen = models.CharField('Entrega Domicilio Origen', choices=SI_NO, max_length=2)
    origen_cuit = models.CharField('Origen CUIT', max_length=11)
    origen_razon_social = models.CharField('Origen: Razon Social', max_length=50)
    emisor_tenedor = models.BooleanField('Emisor es Tenedor')
    origen_domicilio_calle = models.CharField('Origen: Calle de Domicilio', max_length=40)
    origen_domicilio_codigopostal = models.CharField('Origen: Domicilio Codigo Postal', max_length=8)
    origen_domicilio_localidad = models.ForeignKey('Localidad', verbose_name='Localidad de Origen', related_name='cot_localidad_origen')
    origen_domicilio_provincia = models.ForeignKey('Provincia', verbose_name='Provincia de Origen', related_name='cot_provincia_origen', to_field='codigo_arba')
    transportista_cuit = models.CharField('CUIT Transportista', max_length=11)
    patente_vehiculo = models.CharField('Patente Vehiculo', max_length=7, blank=True, default=' ', null=True)
    producto_no_term_dev = models.BooleanField('Productos No Terminados / Devoluciones', default=False)
    importe = models.CharField('Importe', max_length=10)
    codigo_unico_producto = models.CharField('Codigo Unico Producto', max_length=6)
    rentas_codigo_unidad_medida = models.IntegerField('Codigo Unidad Medida', choices=ARBA_MEDIDAS)
    cantidad = models.CharField('Cantidad', max_length=15)
    propio_codigo_producto = models.CharField('Propio Codigo Producto', max_length=25)
    propio_descripcion_producto = models.CharField('Propio Descripcion Producto', max_length=40)
    propio_descripcion_unidad_medida = models.CharField('Propio Descripcion Unidad Medida', max_length=20)
    cantidad_ajustada = models.CharField('Cantidad Ajustada', max_length=15)
    generar_cot = models.BooleanField('Generar COT?', default=False)
    cot_nombre = models.CharField('COT Nombre', max_length=30, blank=True)
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.now)
    numero_comprobante = models.CharField('Numero de Comprobante', max_length=30, blank=True)
    codigo_integridad = models.CharField('Codigo Integridad', max_length=50, blank=True)
    errores = models.TextField('Errores', blank=True)
    estado = models.IntegerField('Estado del COT', choices=COT_ESTADO, default=1, blank=True, null=True)
    file_path = models.CharField('Archivo de Intercambio', max_length=200)
    
    def __unicode__(self):
        return 'Fecha: {}, Nombre: {}, Nro Comprobante: {}'.format(self.fecha, self.cot_nombre, self.numero_comprobante)
        
    def _procesar_condicionales(self, val):
        # Funcion encargada de ajustar los campos condicionales de acuerdo\
        # a los requerimientos de ARBA
        if val:
            return val
        else:
            return ' '
        
    def _procesar_booleanos(self, val):
        # Funcion encargada de ajustar los campos booleano de acuerdo\
        # a los requerimientos de ARBA
        if val:
            return '1'
        else:
            return '0'
        
        
    def generar_archivo(self):
#         registro02 = '02|20080124|91 R999900068148|20080124| |E|0| | |30682115722|COMPUMUNDOS.A.|0|Ruta Prov | |S/N| | | |1200|PUERTO DE ESCOBAR|B| |NO|23246414254|COMPUMUNDO S.A.|0|San Martin 5797| |S/N| | | |1766|TABLADA|B|20045162673| | | | | | |1|1234\r\n'.format()
#         registro02 += '0| | |30682115722|COMPUMUNDOS.A.|0|Ruta Prov | |S/N| | | |1200|PUERTO DE ESCOBAR|B| |NO|23246414254|COMPUMUNDO S.A.|0|San Martin 5797| |S/N| | | |1766|TABLADA|B|20045162673| | | | | | |1|1234\r\n'.format()
#         registro03 = '03|847150|3|100|23891|COMP. SP-3960 VP|UNI DAD| 100\r\n'
        registro01 = '01|{}\r\n'.format(self.cuit_empresa)
        registro02 = '02|{}|'.format(self.fecha_emision)
        registro02 += '{}{}|'.format(self.tipo_comprobante, self.nro_comprobante)
        registro02 += '{}|'.format(self.fecha_salida_transporte)
        registro02 += ' |' # HORA_SALIDA_TRANSPORTE  
        registro02 += '{}|'.format(self.sujeto_generador)
        registro02 += '{}|'.format(self._procesar_booleanos(self.destinatario_consumidor_final))
        registro02 += ' |' # DESTINATARIO_TIPO_DOCUMENT
        registro02 += ' |' # DESTINATARIO_DOCUMENTO
        registro02 += '{}|'.format(self._procesar_condicionales(self.destinatario_cuit))
        registro02 += '{}|'.format(self._procesar_condicionales(self.destinatario_razon_social))
        registro02 += '{}|'.format(self._procesar_booleanos(self.destinatario_tenedor))
        registro02 += '{}|'.format(self.destino_domicilio_calle)
        registro02 += '0|' # DESTINO_DOMICILIO_NUMERO
        registro02 += 'S/N|' # DESTINO_DOMICILIO_COMPLE
        registro02 += ' |' # DESTINO_DOMICILIO_PISO
        registro02 += ' |' # DESTINO_DOMICILIO_DTO
        registro02 += ' |' # DESTINO_DOMICILIO_BARRIO
        registro02 += '{}|'.format(self.destino_domicilio_codigopostal)
        registro02 += '{}|'.format(self.destino_domicilio_localidad.nombre)
        registro02 += '{}|'.format(self.destino_domicilio_provincia.codigo_arba)
        registro02 += ' |' # PROPIO_DESTINO_DOMICILIO_CODIGO
        registro02 += '{}|'.format(self.entrega_domicilio_origen)
        registro02 += '{}|'.format(self.origen_cuit)
        registro02 += '{}|'.format(self.origen_razon_social)
        registro02 += '{}|'.format(self._procesar_booleanos(self.emisor_tenedor))
        registro02 += '{}|'.format(self.origen_domicilio_calle)
        registro02 += '0|' # ORIGEN_DOMICILIO_NUMERO
        registro02 += 'S/N|' # ORIGEN_DOMICILIO_COMPLE
        registro02 += ' |' # ORIGEN_DOMICILIO_PISO
        registro02 += ' |' # ORIGEN_DOMICILIO_DTO
        registro02 += ' |' # ORIGEN_DOMICILIO_BARRIO
        registro02 += '{}|'.format(self.origen_domicilio_codigopostal)
        registro02 += '{}|'.format(self.origen_domicilio_localidad.nombre)
        registro02 += '{}|'.format(self.origen_domicilio_provincia.codigo_arba)
        registro02 += '{}|'.format(self.transportista_cuit)
        registro02 += ' |' # TIPO_RECORRIDO
        registro02 += ' |' # RECORRIDO_LOCALIDAD
        registro02 += ' |' # RECORRIDO_CALLE
        registro02 += ' |' # RECORRIDO_RUTA
        registro02 += '{}|'.format(self._procesar_condicionales(self.patente_vehiculo))
        registro02 += ' |' # PATENTE_ACOPLADO
        registro02 += '{}|'.format(self._procesar_booleanos(self.producto_no_term_dev))
        registro02 += '{}\r\n'.format(self._procesar_condicionales(self.importe))
        
        registro03 = '03|{}|'.format(self.codigo_unico_producto)
        registro03 += '{}|'.format(self.rentas_codigo_unidad_medida)
        registro03 += '{}|'.format(self.cantidad)
        registro03 += '{}|'.format(self.propio_codigo_producto)
        registro03 += '{}|'.format(self.propio_descripcion_producto)
        registro03 += '{}|'.format(self.propio_descripcion_unidad_medida)
        registro03 += '{}\r\n'.format(self.cantidad_ajustada)
        
        registro04 = '04|1\r\n' # Cantidad total de remitos
        
        file_name = 'TB_{}_000000_{}_000001.txt'.format(self.cuit_empresa, self.fecha_emision)
        self.file_path = os.path.join(BASE_DIR, 'data/arba', file_name)
        archivo = open(self.file_path, 'w+')
        archivo.write(registro01)
        archivo.write(registro02)
        archivo.write(registro03)
        archivo.write(registro04)
        archivo.close()
        
    def procesar_errores(self, errores):
        errores = errores.replace('_', ' ').replace('Mensaje Error', 'mensaje_error')
        errores = errores.replace('inv??lido', 'inválido') 
        return errores
        
    def solicitar_cot(self):
        self.generar_archivo()
        # TODO: Utilizar las credenciales provistas por el usuario
        cot = get_wscot_client('20244416722', '431108')
        cot.Conectar()
        cot.PresentarRemito(self.file_path)
        self.numero_comprobante = cot.NumeroComprobante
        self.codigo_integridad = cot.CodigoIntegridad
        errores = []
        while cot.LeerValidacionRemito():
            while cot.LeerErrorValidacion():
                remito = {}
                remito['Nro'] = cot.NumeroUnico
                remito['Codigo Error'] = cot.CodigoError
                remito['Mensaje Error'] = cot.MensajeError
                errores.append(remito)
        self.errores = self.procesar_errores(json.dumps(errores))
        if not errores and self.numero_comprobante:
            self.estado = COT_ESTADO_GENERADO
        else:
            self.estado = COT_ESTADO_ERROR
#     def save(self, **kwargs):
#         if self.generar_cot and not self.numero_comprobante:
#             self.solicitar_cot()
#         return super(COT, self).save(**kwargs)
        
    class Meta:
        verbose_name = 'COT'
        verbose_name_plural = 'COTs'
    
    

class CTG(models.Model):
    '''
    Entidad que representa un Codigo de Trazabilidad de Granos
    '''
    CTG_ESTADO = (
        (CTG_ESTADO_PENDIENTE, 'Parcial'),
        (CTG_ESTADO_GENERADO, 'Generado'),
        (CTG_ESTADO_ANULADO, 'Anulado'),
        (CTG_ESTADO_ARRIBADO, 'Arribado')
    )
    CTG_ACCION = (
        (CTG_ACCION_PARCIAL, 'CTG Parcial'),
        (CTG_ACCION_SOLICITAR, 'Solicitar CTG')
        )
    
    usuario_solicitante = models.ForeignKey(User, verbose_name='Usuario Solicitante')
    numero_carta_de_porte = models.CharField('*Nro Carta de Porte', max_length=12, blank=True, null=True, unique=True)
    codigo_especie = models.ForeignKey('Especie', verbose_name='*Codigo Especie', blank=True, null=True)
    cuit_remitente = models.ForeignKey(Entidad, verbose_name='Cuit Remitente Comercial', related_name='ctg_remitente', blank=True, null=True)
    #cuit_remitente = models.CharField('Cuit Remitente Comercial', max_length=11, null=True, blank=True)
    remitente_comercial_como_canjeador = models.BooleanField('Rte Comercial actua como Canjeador?', default=False)
    remitente_comercial_como_productor = models.BooleanField('Rte Comercial actua como Productor?', default=False)
    cuit_destino = models.ForeignKey(Entidad, verbose_name='*Cuit Destino', related_name='ctg_destino', blank=True, null=True)
    #cuit_destino = models.CharField('*Cuit Destino', max_length=11, null=True, blank=True)
    cuit_destinatario = models.ForeignKey(Entidad, verbose_name='*Cuit Destinatario', related_name='ctg_destinatario', blank=True, null=True)
    #cuit_destinatario = models.CharField('*Cuit Destinatario', max_length=11, null=True, blank=True)
    cuit_transportista = models.ForeignKey(Entidad, verbose_name='Cuit Tranportista', blank=True, null=True, related_name='ctg_transportista')
    #cuit_transportista = models.CharField('*Cuit Transportista', max_length=11, null=True, blank=True) 
    cuit_corredor = models.ForeignKey(Entidad, verbose_name='Cuit Corredor', blank=True, null=True, related_name='ctg_corredor')
    codigo_localidad_origen = models.ForeignKey('Localidad', verbose_name='*Codigo Localidad Origen', related_name='ctg_localidad_origen', blank=True, null=True)
    codigo_localidad_destino = models.ForeignKey('Localidad', verbose_name='*Codigo Localidad Destino', related_name='ctg_localidad_destino', blank=True, null=True)
    codigo_cosecha = models.ForeignKey('Cosecha', verbose_name='*Codigo Cosecha', blank=True, null=True)
    peso_neto_carga = models.PositiveIntegerField('*Peso Neto de Carga', blank=True, null=True)
    cant_horas = models.PositiveIntegerField('Cantidad de Horas', blank=True, null=True)
    patente_vehiculo = models.CharField('*Patente Vehiculo', max_length=30, blank=True, null=True)
    km_a_recorrer = models.PositiveIntegerField('*Km a Recorrer', blank=True, null=True)
    #remitente_comercial_como_canjeador = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    #remitente_comercial_como_productor = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    turno = models.CharField('Turno', max_length=50, blank=True, null=True)
    estado = models.IntegerField('Estado del CTG', choices=CTG_ESTADO, default=1, blank=True, null=True)
    geolocalizacion = models.CharField('Geo Localizacion de la Solicitud', blank=True, max_length=150)
    numero_ctg = models.CharField('Nro CTG', max_length=50, blank=True)
    observaciones = models.CharField('Observaciones', blank=True, null=True, max_length=200)
    fechahora = models.CharField('Fecha y Hora', blank=True, null=True, max_length=200)
    vigenciadesde = models.CharField('Vigencia Desde', blank=True, null=True, max_length=200)
    vigenciahasta = models.CharField('Vigencia Hasta', blank=True, null=True, max_length=200)
    tarifareferencia = models.CharField('Tarifa Referencia', blank=True, null=True, max_length=200)
    errores = models.CharField('Errores', blank=True, null=True, max_length=200)
    controles = models.CharField('Controles', blank=True, null=True, max_length=200)
    codigo_operacion = models.CharField('Codigo Operacion', blank=True, null=True, max_length=100)
    accion = models.IntegerField('Accion', choices=CTG_ACCION, default=1)
    operacion = models.ForeignKey('Operacion', null=True, blank=True, related_name='ctg')
    nombre = models.CharField('Nombre de CTG', null=True, blank=True, max_length=50)
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.now, null=True)
    
    '''
    def registrar_operacion(self, tipo_operacion):
        # Funcion encargada de registrar la operacion en el caso que necesario
        if not self.operacion:
            self.operacion = Operacion.objects.create(nombre=self.nombre)
        self.operacion.tipo_operacion = tipo_operacion
        self.operacion.datos = {}
    '''     
    
    def save(self, **kwargs):
        # Parche para solicitar cuando se crea registro desde Admin
#         if (self.estado==CTG_ESTADO_PENDIENTE and self.accion==CTG_ACCION_SOLICITAR):
#             self.solicitar_ctg()
        return super(CTG, self).save(**kwargs)
    
    def has_related_object(self, related_name):
        return hasattr(self, related_name)
    
    def __unicode__(self):
        return "Carta Porte: {}, Ctg: {}, Estado: {}".format(self.numero_carta_de_porte, self.numero_ctg, self.estado)
    
    def anular_ctg(self):
        if self.numero_carta_de_porte and self.numero_ctg:
            token = obtener_afip_token()
            wsctg = get_wsctg_client()
            wsctg.HOMO = HOMO
            wsctg.WSDL = WSCTG_WSDL
            wsctg.Conectar()
            wsctg.SetTicketAcceso(token)
            wsctg.Cuit = CUIT_SOLICITANTE
            wsctg.AnularCTG(self.numero_carta_de_porte, self.numero_ctg)
            
            self.numero_carta_de_porte = wsctg.CartaPorte
            self.numero_ctg = wsctg.NumeroCTG
            self.fechahora = wsctg.FechaHora
            self.codigo_operacion = wsctg.CodigoOperacion
        self.estado = CTG_ESTADO_ANULADO
        self.save()
    
    def _simular_ctg(self):
        from random import randint
        self.numero_ctg = randint(9100200, 49100200)
        self.fechahora = timezone.datetime.now()
        self.vigenciadesde = timezone.localdate()
        self.vigenciahasta = timezone.localdate() + timezone.timedelta(days=5)
        self.tarifareferencia = '{}.{}'.format(randint(100, 999), randint(0, 99))
        self.errores = []
        self.controles = []
        if not self.controles:
            self.estado = CTG_ESTADO_GENERADO
    
    def solicitar_ctg(self):
        #return self._simular_ctg()
        
        token = obtener_afip_token()
        wsctg = get_wsctg_client()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        wsctg.Cuit = CUIT_SOLICITANTE
        
        cuit_transportista = self.cuit_transportista.cuit if self.cuit_transportista else None 
        cuit_corredor = self.cuit_corredor.cuit if self.cuit_corredor else None 
        cuit_remitente = self.cuit_remitente.cuit if self.cuit_remitente else None 
        remitente_comercial_como_canjeador = cuit_canjeador = cuit_remitente if self.remitente_comercial_como_canjeador else None 
        remitente_comercial_como_productor = cuit_canjeador = cuit_remitente if self.remitente_comercial_como_productor else None 
        
        numero_ctg = wsctg.SolicitarCTGInicial(self.numero_carta_de_porte, 
                                              self.codigo_especie.codigo,
                                              cuit_canjeador, 
                                              self.cuit_destino.cuit, 
                                              self.cuit_destinatario.cuit, 
                                              self.codigo_localidad_origen.codigo, 
                                              self.codigo_localidad_destino.codigo, 
                                              self.codigo_cosecha.codigo, 
                                              self.peso_neto_carga, 
                                              self.cant_horas, 
                                              self.patente_vehiculo, 
                                              cuit_transportista, 
                                              self.km_a_recorrer, 
                                              remitente_comercial_como_canjeador, 
                                              cuit_corredor, 
                                              remitente_comercial_como_productor, 
                                              self.turno)
        self.numero_ctg = numero_ctg
        self.observaciones = wsctg.Observaciones
        self.fechahora = wsctg.FechaHora
        self.vigenciadesde = wsctg.VigenciaDesde
        self.vigenciahasta = wsctg.VigenciaHasta
        self.tarifareferencia = wsctg.TarifaReferencia
        self.errores = json.dumps(self.procesar_errores(wsctg.Errores))
        self.controles = wsctg.Controles
        if self.numero_ctg:
            self.estado = CTG_ESTADO_GENERADO
        if self.errores:
            self.estado = CTG_ESTADO_ERROR
    
    def procesar_errores(self, afip_errors):
        ret = []
        for error in afip_errors:
            ret.append(unicode(error.replace('<br>', '\n')))
        return ret
    
    class Meta:
        verbose_name = 'CTG'
        verbose_name_plural = 'CTGs'
        
    
class Operacion(models.Model):
    '''
    Representa todas las operacion ante AFIP realizadas por el usuario
    '''    
    TIPO_OPERACION = (
        (1, 'CTG Solicitado'),
        (2, 'CTG carga parcial'),
        (3, 'CTG Anulado'),
        (4, 'COT')
    )
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.now)
    nombre = models.CharField('Nombre de Operacion', max_length=120, blank=True)
    tipo_operacion = models.CharField('Tipo de Operacion', choices=TIPO_OPERACION, max_length=20)
    datos = models.TextField('Datos de la Operacion')
    
    def __unicode__(self):
        return self.tipo_operacion
    
    class Meta:
        verbose_name = 'Operacion'
        verbose_name_plural = 'Operaciones'
    
        
class Cosecha(models.Model):
    codigo = models.PositiveIntegerField('Codigo', primary_key=True)
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Cosecha'
        verbose_name_plural = 'Cosechas'
        

class Especie(models.Model):
    codigo = models.PositiveIntegerField('Codigo', primary_key=True)
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'


class Establecimiento(models.Model):
    codigo = models.PositiveIntegerField('Codigo', primary_key=True)
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'
        
        
class Provincia(models.Model):
    codigo = models.PositiveIntegerField('Codigo', primary_key=True)
    codigo_arba = models.CharField('Codigo ARBA', max_length=1, unique=True)
    nombre = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        
    
class Localidad(models.Model):
    provincia = models.ForeignKey(Provincia)
    codigo = models.PositiveIntegerField('Codigo', primary_key=True)
    nombre = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        
        
    
'''
@receiver(post_save, sender=CTG)
def solicitar_ctg_inicial(**kwargs):
    pass
    obj = kwargs['instance']
    token = obj.usuario_solicitante.credenciales.obtener_afip_token()
    wsctg = WSCTG()
    wsctg.HOMO = HOMO
    wsctg.WSDL = WSCTG_WSDL
    wsctg.Conectar()
    wsctg.SetTicketAcceso(token)
    wsctg.Cuit = CUIT_SOLICITANTE
    
    cuit_transportista = obj.cuit_transportista.cuit if obj.cuit_transportista else None 
    cuit_corredor = obj.cuit_corredor.cuit if obj.cuit_corredor else None 
    cuit_remitente = obj.cuit_remitente.cuit if obj.cuit_remitente else None 
    remitente_comercial_como_canjeador = cuit_canjeador = cuit_remitente if obj.remitente_comercial_como_canjeador else None 
    remitente_comercial_como_productor = cuit_canjeador = cuit_remitente if obj.remitente_comercial_como_productor else None 
    
    remitente_comercial_como_canjeador = ''
    remitente_comercial_como_productor = ''
    
    numero_ctg = wsctg.SolicitarCTGInicial(obj.numero_carta_de_porte, 
                                          obj.codigo_especie.codigo,
                                          cuit_canjeador, 
                                          obj.cuit_destino.cuit, 
                                          obj.cuit_destinatario.cuit, 
                                          obj.codigo_localidad_origen.codigo, 
                                          obj.codigo_localidad_destino.codigo, 
                                          obj.codigo_cosecha.codigo, 
                                          obj.peso_neto_carga, 
                                          obj.cant_horas, 
                                          obj.patente_vehiculo, 
                                          cuit_transportista, 
                                          obj.km_a_recorrer, 
                                          str(remitente_comercial_como_canjeador), 
                                          cuit_corredor, 
                                          str(remitente_comercial_como_productor), 
                                          obj.turno)
    obj.numero_ctg = numero_ctg
    obj.observaciones = wsctg.Observaciones
    obj.fechahora = wsctg.FechaHora
    obj.vigenciadesde = wsctg.VigenciaDesde
    obj.vigenciahasta = wsctg.VigenciaHasta
    obj.tarifareferencia = wsctg.TarifaReferencia
    obj.errores = wsctg.Errores
    obj.controles = wsctg.Controles
    obj.save()
    
    Operacion.objects.create(ctg=obj, tipo_operacion=1)
'''