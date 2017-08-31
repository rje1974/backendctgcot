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
from cotctg.backend.constants import WSAA_WSDL, WSAA_URL


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


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
        wsaa.WSDL = WSAA_WSDL
        wsaa.WSAAURL = WSAA_URL
        self.wsaa_token = wsaa.Autenticar("wsctg", cert, key, debug=DEBUG)
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
    numero_carta_de_porte = models.PositiveIntegerField('Nro Carta de Porte', validators=[MaxValueValidator(999999999999)])
    cuit_remitente = models.ForeignKey(Entidad, verbose_name='Cuit Remitente Comercial', related_name='ctg_remitente')
    remitente_comercial_como_canjeador = models.BooleanField('Rte Comercial actua como Canjeador?', default=False)
    remitente_comercial_como_productor = models.BooleanField('Rte Comercial actua como Productor?', default=False)
    cuit_destino = models.ForeignKey(Entidad, verbose_name='Cuit Destino', related_name='ctg_destino')
    cuit_destinatario = models.ForeignKey(Entidad, verbose_name='Cuit Destinatario', related_name='ctg_destinatario')
    cuit_transportista = models.ForeignKey(Entidad, verbose_name='Cuit Tranportista', blank=True, related_name='ctg_transportista') 
    cuit_corredor = models.ForeignKey(Entidad, verbose_name='Cuit Corredor', blank=True, related_name='ctg_corredor')
    codigo_localidad_origen = models.PositiveIntegerField('Codigo Localidad Origen')
    codigo_localidad_destino = models.PositiveIntegerField('Codigo Localidad Destino')
    codigo_cosecha = models.PositiveIntegerField('Codigo Cosecha')
    peso_neto_carga = models.PositiveIntegerField('Peso Neto de Carga')
    cant_horas = models.PositiveIntegerField('Cantidad de Horas', blank=True)
    patente_vehiculo = models.CharField('Patente Vehiculo', max_length=30, blank=True)
    km_a_recorrer = models.PositiveIntegerField('Km a Recorrer', blank=True)
    #remitente_comercial_como_canjeador = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    #remitente_comercial_como_productor = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    turno = models.CharField('Turno', max_length=50, blank=True)
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
        return self.descripcion
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        
    
class Localidad(models.Model):
    provincia = models.ForeignKey(Provincia)
    codigo = models.PositiveIntegerField('Codigo')
    nombre = models.CharField('Descripcion', max_length=100)
    
    def __unicode__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        
        
        
@receiver(post_save, sender=CTG)
def solicitar_ctg_inicial(instance, **kwargs):
    token = instance.usuario_solicitante.credenciales.obtener_afip_token()
    wsctg = WSCTG()
    wsctg.Conectar()
    wsctg.SetTicketAcceso(token)
    wsctg.Cuit = CUIT_SOLICITANTE
    
    cuit_transportista = instance.cuit_transportista.cuit if instance.has_related_object('ctg_transportista') else None
    cuit_corredor = instance.cuit_corredor.cuit if instance.has_related_object('ctg_corredor') else None
    '''
    # guardar estos datos
    print "Observiacion: ", wsctg.Observaciones
    print "Fecha y Hora", wsctg.FechaHora
    print "Vigencia Desde", wsctg.VigenciaDesde
    print "Vigencia Hasta", wsctg.VigenciaHasta
    print "Tarifa Referencia: ", wsctg.TarifaReferencia
    print "Errores:", wsctg.Errores
    print "Controles:", wsctg.Controles
    
    cuit_canjeador = ''
    
    
    numero_ctg = wsctg.SolicitarCTGInicial(instance.numero_carta_de_porte, 
                              instance.codigo_especie, 
                              cuit_canjeador, 
                              cuit_destino, 
                              cuit_destinatario, 
                              instance.codigo_localidad_origen, 
                              instance.codigo_localidad_destino, 
                              instance.codigo_cosecha, 
                              instance.peso_neto_carga, 
                              instance.cant_horas, 
                              instance.patente_vehiculo, 
                              cuit_transportista, 
                              instance.km_a_recorrer, 
                              remitente_comercial_como_canjeador, 
                              cuit_corredor, 
                              remitente_comercial_como_productor, 
                              instance.turno)

    '''