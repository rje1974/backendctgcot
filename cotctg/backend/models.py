# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from pyafipws.wsaa import WSAA
from pyafipws.wsctg import WSCTG
from .constants import HOMO, DEBUG, CUIT_SOLICITANTE
from django.core.validators import MaxValueValidator
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .constants import WSAA_WSDL, WSAA_URL, CACERT
from django.db.models.fields.related import ForeignKey
from backend.constants import WSCTG_WSDL


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.usuario.id, filename)


class Credencial(models.Model):
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
    usuario_solicitante = models.ManyToManyField(User, verbose_name='Usuario Solicitante')
    nombre = models.CharField('Nombre de Entidad', max_length=120)
    cuit = models.PositiveIntegerField('CUIT', validators=[MaxValueValidator(99999999999)])
    actua_como = models.IntegerField('Actúa como', choices=ACTUA_COMO)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        

class CTG(models.Model):
    '''
    Entidad que representa un Codigo de Trazabilidad de Granos
    '''
    CTG_ESTADO = (
        (1, 'Sin Generar'),
        (2, 'Generado'),
        (3, 'Datos Pendientes'),
        (4, 'Anulado'),
        (5, 'Arribado')
    )
    
    usuario_solicitante = models.ForeignKey(User, verbose_name='Usuario Solicitante')
    numero_carta_de_porte = models.CharField('Nro Carta de Porte', max_length=12)
    codigo_especie = models.ForeignKey('Especie', verbose_name='Codigo Especie')
    cuit_remitente = models.ForeignKey(Entidad, verbose_name='Cuit Remitente Comercial', related_name='ctg_remitente', blank=True, null=True)
    remitente_comercial_como_canjeador = models.BooleanField('Rte Comercial actua como Canjeador?', default=False)
    remitente_comercial_como_productor = models.BooleanField('Rte Comercial actua como Productor?', default=False)
    cuit_destino = models.ForeignKey(Entidad, verbose_name='Cuit Destino', related_name='ctg_destino')
    cuit_destinatario = models.ForeignKey(Entidad, verbose_name='Cuit Destinatario', related_name='ctg_destinatario')
    cuit_transportista = models.ForeignKey(Entidad, verbose_name='Cuit Tranportista', blank=True, null=True, related_name='ctg_transportista') 
    cuit_corredor = models.ForeignKey(Entidad, verbose_name='Cuit Corredor', blank=True, null=True, related_name='ctg_corredor')
    codigo_localidad_origen = models.ForeignKey('Localidad', verbose_name='Codigo Localidad Origen', related_name='ctg_localidad_origen')
    codigo_localidad_destino = models.ForeignKey('Localidad', verbose_name='Codigo Localidad Destino', related_name='ctg_localidad_destino')
    codigo_cosecha = models.ForeignKey('Cosecha', verbose_name='Codigo Cosecha')
    peso_neto_carga = models.PositiveIntegerField('Peso Neto de Carga')
    cant_horas = models.PositiveIntegerField('Cantidad de Horas', blank=True, null=True)
    patente_vehiculo = models.CharField('Patente Vehiculo', max_length=30, blank=True, null=True)
    km_a_recorrer = models.PositiveIntegerField('Km a Recorrer')
    #remitente_comercial_como_canjeador = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    #remitente_comercial_como_productor = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    turno = models.CharField('Turno', max_length=50, blank=True, null=True)
    estado = models.IntegerField('Estado del CTG', choices=CTG_ESTADO, default=1)
    geolocalizacion = models.CharField('Geo Localizacion de la Solicitud', blank=True, max_length=150)
    numero_ctg = models.CharField('Nro CTG', max_length=50, blank=True)
    observaciones = models.CharField('Observaciones', blank=True, null=True, max_length=200)
    fechahora = models.CharField('Fecha y Hora', blank=True, null=True, max_length=200)
    vigenciadesde = models.CharField('Vigencia Desde', blank=True, null=True, max_length=200)
    vigenciahasta = models.CharField('Vigencia Hasta', blank=True, null=True, max_length=200)
    tarifareferencia = models.CharField('Tarifa Referencia', blank=True, null=True, max_length=200)
    errores = models.CharField('Errores', blank=True, null=True, max_length=200)
    controles = models.CharField('Controles', blank=True, null=True, max_length=200)
    
    def has_related_object(self, related_name):
        return hasattr(self, related_name)
    
    def __unicode__(self):
        return "Ctg: {}, Estado: {}".format(self.numero_ctg, self.estado)
    
    def _obtener_ctg(self):
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
    
    def save(self, **kwargs):
        if not self.numero_ctg:
            self._obtener_ctg()
        
        #Operacion.objects.create(ctg=obj, tipo_operacion=1)
        return models.Model.save(self, **kwargs)
    
    class Meta:
        verbose_name = 'CTG'
        verbose_name_plural = 'CTGs'
        
    
class Operacion(models.Model):
    '''
    Representa todas las operacion ante AFIP realizadas por el usuario
    '''    
    TIPO_OPERACION = (
        (1, 'Solicitud CTG desde Inicio'),
        (2, 'Solicitud CTG dato Pendiente'),
        (3, 'Anular CTG')
    )
    fecha = models.DateTimeField('Fecha de Operacion', default=timezone.now)
    tipo_operacion = models.CharField('Tipo de Operacion', choices=TIPO_OPERACION, max_length=20)
    ctg = models.ForeignKey(CTG, null=True)
    
    def __unicode__(self):
        return self.tipo_operacion
    
    class Meta:
        verbose_name = 'Operacion'
        verbose_name_plural = 'Operaciones'
    
        
class Cosecha(models.Model):
    codigo = models.PositiveIntegerField('Codigo')
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Cosecha'
        verbose_name_plural = 'Cosechas'
        

class Especie(models.Model):
    codigo = models.PositiveIntegerField('Codigo')
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'


class Establecimiento(models.Model):
    codigo = models.PositiveIntegerField('Codigo')
    descripcion = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'
        
        
class Provincia(models.Model):
    codigo = models.PositiveIntegerField('Codigo')
    nombre = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        
    
class Localidad(models.Model):
    provincia = models.ForeignKey(Provincia)
    codigo = models.PositiveIntegerField('Codigo')
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