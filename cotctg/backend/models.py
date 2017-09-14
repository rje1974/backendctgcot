# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from pyafipws.wsaa import WSAA
from pyafipws.wsctg import WSCTG
from .constants import HOMO, DEBUG, CUIT_SOLICITANTE
from django.utils import timezone
from .constants import WSAA_WSDL, WSAA_URL, CACERT
from backend.constants import WSCTG_WSDL, CTG_ESTADO_GENERADO\
    , CTG_ESTADO_PENDIENTE, CTG_ESTADO_ANULADO,\
    CTG_ESTADO_ARRIBADO, CTG_ACCION_SOLICITAR, CTG_ACCION_PARCIAL
from django.utils.datetime_safe import datetime


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.usuario.id, filename)


class Credencial(models.Model):
    '''
    Representa las credenciales de autenticacion del usuario ante AFIP y ARBA
    '''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credenciales')
    key = models.FileField('Clave Privada', upload_to=user_directory_path)
    certificado = models.FileField('Certificado', upload_to=user_directory_path)
    certificado_texto = models.TextField('Text de Certificado', blank=True)
    wsaa_token = models.FileField('Token WSAA (TA)', blank=True)

    class Meta:
        verbose_name = 'Credenciales AFIP'
        verbose_name_plural = 'Credenciales AFIP'

    def _get_key_file(self):
        pass
    
    
    def _get_cert_file(self):
        pass
    
    @classmethod
    def obtener_afip_token(self):
        cert = '/home/hugo/development/cotctg/cotctg/backend/ctg.crt' 
        key = '/home/hugo/development/cotctg/cotctg/backend/privada.key'
        wsaa = WSAA()
        wsaa.HOMO = HOMO
        wsaa.DEBUG = DEBUG
        wsaa.WSAAURL = WSAA_URL
        self.wsaa_token = wsaa.Autenticar("wsctg", cert, key, wsdl=WSAA_WSDL, debug=DEBUG, cacert=CACERT)
        return self.wsaa_token


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
        
        
class Provincia_ARBA(models.Model):
    codigo = models.CharField('Codigo', max_length=1, primary_key=True)
    descripcion = models.CharField('Nombre', max_length=25)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Provicia ARBA'
        verbose_name_plural = 'Provincias ARBA'
        
        
class COT(models.Model):
    '''
    Representa un Codigo de Operacion Traslado/Transporte
    (Por el momento se incluyen solo los campos requeridos)
    
    Campos que se agregan manualmente al txt:
    tipo_registro
    cantidad_total_remitos
    '''
    SUJETO_GENERADOR =(
            ('E', 'Emisor'),
            ('D', 'Destinatario')
        )
    SI_NO = (
            ('SI', 'Si'),
            ('NO', 'No')
        )
    ARBA_MEDIDAS = (
        (1, 'Kilogramos'),
        (2, 'Litros'),
        (3, 'Unidades'),
        (4, 'Metros Cuadrados'),
        (5, 'Metros'),
        (6, 'Metros Cubicos'),
        (7, 'Pares'),        
        )
    
    cuit_empresa = models.CharField('CUIT Empresa', max_length=11)
    fecha_emision = models.DateField('Fecha Emision')
    codigo_unico = models.CharField('Codigo Unico', max_length=16)
    fecha_salida_transporte = models.DateField('Fecha Salida Transporte')
    sujeto_generador = models.CharField('Sujeto Generador', choices=SUJETO_GENERADOR, max_length=1)
    destinatario_consumidor_final = models.BooleanField('Destinatario Consumidor Final?')
    destinatario_tenedor = models.BooleanField('Destinatario es Tenedor')
    destino_domicilio_calle = models.CharField('Destino: Calle de Domicilio', max_length=40)
    destino_domicilio_codigopostal = models.CharField('Destino: Codigo Postal', max_length=8)
    destino_domicilio_localidad = models.CharField('Destino: Localidad', max_length=50)
    destino_domicilio_provincia = models.ForeignKey('Provincia_ARBA', related_name='provincia_destino')
    entrega_domicilio_origen = models.CharField('Entrega Domicilio Origen', choices=SI_NO, max_length=2)
    origen_cuit = models.CharField('Origen CUIT', max_length=11)
    origen_razon_social = models.CharField('Origen: Razon Social', max_length=50)
    emisor_tenedor = models.BooleanField('Emisor es Tenedor')
    origen_domicilio_calle = models.CharField('Origen: Calle de Domicilio', max_length=40)
    origen_domicilio_codigopostal = models.CharField('Origen: Domicilio Codigo Postal', max_length=8)
    origen_domicilio_localidad = models.CharField('Origen: Localidad', max_length=50)
    origen_domicilio_provincia = models.ForeignKey('Provincia_ARBA', related_name='provincia_origen')
    transportista_cuit = models.CharField('CUIT Transportista', max_length=11)
    producto_no_term_dev = models.BooleanField('Productos No Terminados / Devoluciones', default=False)
    importe = models.CharField('Importe', max_length=10)
    codigo_unico_producto = models.CharField('Codigo Unico Producto', max_length=6)
    rentas_codigo_unidad_medida = models.CharField('Codigo Unidad Medida', max_length=1, choices=ARBA_MEDIDAS)
    cantidad = models.CharField('Cantidad', max_length=15)
    propio_codigo_producto = models.CharField('Propio Codigo Producto', max_length=25)
    propio_descripcion_producto = models.CharField('Propio Descripcion Producto', max_length=40)
    propio_descripcion_unidad_medida = models.CharField('Propio Descripcion Unidad Medida', max_length=20)
    cantidad_ajustada = models.CharField('Cantidad Ajustada', max_length=15)
    generar_cot = models.BooleanField('Generar COT?', default=False)
    cot_nombre = models.CharField('COT Nombre', max_length=30)
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.datetime.now)
    
    def __unicode__(self):
        return self.cot_nombre
        
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
    numero_carta_de_porte = models.CharField('*Nro Carta de Porte', max_length=12, blank=True, null=True)
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
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.localdate, null=True)
    
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
        if (self.estado==CTG_ESTADO_PENDIENTE and self.accion==CTG_ACCION_SOLICITAR):
            self.solicitar_ctg()
        return super(CTG, self).save(**kwargs)
    
    def has_related_object(self, related_name):
        return hasattr(self, related_name)
    
    def __unicode__(self):
        return "Carta Porte: {}, Ctg: {}, Estado: {}".format(self.numero_carta_de_porte, self.numero_ctg, self.estado)
    
    def anular_ctg(self):
        if self.numero_carta_de_porte and self.numero_ctg:
            token = self.usuario_solicitante.credenciales.obtener_afip_token()
            wsctg = WSCTG()
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
        return self._simular_ctg()
        
        token = self.usuario_solicitante.credenciales.obtener_afip_token()
        wsctg = WSCTG()
        wsctg.HOMO = HOMO
        wsctg.WSDL = WSCTG_WSDL
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
        self.errores = wsctg.Errores
        self.controles = wsctg.Controles
        # TODO: Revisar correcta logica
        if not self.controles:
            self.estado = CTG_ESTADO_GENERADO
    
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