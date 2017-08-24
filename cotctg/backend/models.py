# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from pyafipws.wsaa import WSAA
from pyafipws.wsctg import WSCTG


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Credential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.FileField('Clave Privada', upload_to=user_directory_path)
    certificate = models.FileField('Certificado', upload_to=user_directory_path)
    certificate_text = models.TextField('Text de Certificado', blank=True)
    wsaa_token = models.FileField('Token WSAA (TA)', blank=True)

    class Meta:
        verbose_name = 'Credenciales AFIP'
        verbose_name_plural = 'Credenciales AFIP'

    def _get_key_file(self):
        pass
    
    
    def _get_cert_file(self):
        pass
    
    @classmethod
    def get_auth_token(self):
        wsaa = WSAA()
        wsaa.HOMO = True
        wsaa.DEBUG = True
        import ipdb; ipdb.set_trace()
        cert = '/home/hugo/desarrollo/juaneduardoriva/cotctg/cotctg/media/user_2/ctg.crt' 
        key = '/home/hugo/desarrollo/juaneduardoriva/cotctg/cotctg/media/user_2/privada.key'
        self.wsaa_token = wsaa.Autenticar("wsctg", cert, key, debug=True)
        self.save()
        return self.wsaa_token

class Company(models.Model):
    COMPANY_TYPE = ((1, 'Empresa de Origen'),
                    (2, 'Empresa de Destino'))
    
    
    nombre = models.CharField('Nombre de Empresa', max_length=120)
    cuit = models.CharField('CUIT', max_length=20)
    company_type = models.IntegerField('Tipo de Empresa', choices=COMPANY_TYPE)
    default = models.BooleanField('Marcar como Principal', default=False)
    
    
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
        (5, 'Arribado'))
    
    usuario_solicitante = models.ForeignKey(User, verbose_name='Usuario Solicitante')
    numero_carta_de_porte = models.CharField('Nro Carta de Porte', max_length=50)
    numero_ctg = models.CharField('Nro CTG', max_length=50, blank=True)
    cuit_canjeador = models.ForeignKey(Company, verbose_name='Cuit Canjeador', related_name='ctg_cajeador', blank=True)
    cuit_destino = models.ForeignKey(Company, verbose_name='Cuit Destino', related_name='ctg_destino')
    cuit_destinatario = models.ForeignKey(Company, verbose_name='Cuit Destinatario', related_name='ctg_destinatario')
    cuit_transportista = models.ForeignKey(Company, verbose_name='Cuit Tranportista', blank=True, related_name='ctg_transportista') 
    cuit_corredor = models.ForeignKey(Company, verbose_name='Cuit Corredor', blank=True, related_name='ctg_corredor')
    codigo_localidad_origen = models.PositiveIntegerField('Codigo Localidad Origen')
    codigo_localidad_destino = models.PositiveIntegerField('Codigo Localidad Destino')
    codigo_cosecha = models.PositiveIntegerField('Codigo Cosecha')
    peso_neto_carga = models.PositiveIntegerField('Peso Neto de Carga')
    cant_horas = models.PositiveIntegerField('Cantidad de Horas', blank=True)
    patente_vehiculo = models.CharField('Patente Vehiculo', max_length=30, blank=True)
    km_a_recorrer = models.PositiveIntegerField('Km a Recorrer', blank=True)
    remitente_comercial_como_canjeador = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    remitente_comercial_como_productor = models.CharField('Remitente comercial Canjeador', max_length=100, blank=True) 
    turno = models.CharField('Turno', max_length=50, blank=True)
    estado = models.IntegerField('Estado del CTG', choices=CTG_ESTADO, default=1)
    fecha = models.DateField('Fecha de Obtencion del CTG', blank=True)
    geolocalizacion = models.CharField('Geo Localizacion de la Solicitud', blank=True, max_length=150)
    
    
    def __unicode__(self):
        return "Ctg: {}, Estado: {}".format(self.numero_ctg, self.estado)
    
    def save(self, **kwargs):
        token = self.usuario_solicitante.credential.get_auth_token()
        wsctg = WSCTG()
        wsctg.Conectar()
        wsctg.SetTicketAcceso(token)
        #wsctg.Cuit = CUIT
        return models.Model.save(self, **kwargs)
    
    class Meta:
        verbose_name = 'CTG'
        verbose_name_plural = 'CTGs'