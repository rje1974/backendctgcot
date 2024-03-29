'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.serializers import ModelSerializer
from backend.models import Localidad, Provincia, CTG, Entidad, Cosecha, Especie, \
    Establecimiento, COT, Perfil
from backend.constants import CTG_ACCION_SOLICITAR
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from rest_framework.exceptions import ValidationError
from rest_framework import fields, serializers
from datetime import datetime
from backend.utils import obtener_fecha_frontend, validar_cuit


class ProvinciaSerializer(ModelSerializer):

    class Meta:
        model = Provincia
        fields = ('nombre',)


class LocalidadSerializer(ModelSerializer):
    provincia = ProvinciaSerializer(read_only=True)

    class Meta:
        model = Localidad
        depth = 2
        fields = ('codigo', 'nombre', 'provincia',)
        
    def to_representation(self, instance):
        rep = super(LocalidadSerializer, self).to_representation(instance)
        rep['descripcion'] = '{} - {}'.format(rep.get('nombre'), rep.get('provincia').get('nombre'))
        rep.pop('nombre')
        rep.pop('provincia')
        return rep 


class PerfilSerializer(ModelSerializer):
    alias = fields.CharField(required=False, allow_blank=True)
    usuario_arba = fields.CharField(required=False, allow_blank=True)
    pass_arba = fields.CharField(required=False, allow_blank=True)
    cuit_solicitante = fields.IntegerField(allow_null=True)
#     user = fields.ReadOnlyField()

    def create(self, validated_data):
        perfil = Perfil.objects.create(**validated_data)
        return perfil
    
    class Meta:
        model = Perfil
        exclude = ('credenciales_produccion',)


class COTSerializer(FriendlyErrorMessagesMixin, ModelSerializer):
    fecha_salida_transporte = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    
    def get_fecha(self, obj):
        return obtener_fecha_frontend(obj)
    
    def get_fecha_salida_transporte(self, obj):
        return obtener_fecha_frontend(obj)

    def create(self, validated_data):
        obj = COT.objects.create(**validated_data)
        if validated_data.get('generar_cot'):
            obj.solicitar_cot()
        return obj

    def validate(self, data):
        """
        Aplica todas las validaciones necesarias para ARBA.
        """
        if data['destinatario_consumidor_final'] == 0:
            if not data.get('destinatario_cuit'):
                raise ValidationError("Si el destinatario no es Consumidor Final, debe ingresar el Cuit del mismo")
            else:
                if data['sujeto_generador'] in 'D':
                    if not data['destinatario_cuit'] == data['cuit_empresa']:
                        raise ValidationError("Si Sujeto Generador es Destinatario, el Cuit Destinatario debe ser igual al Cuit Empresa")
            if not data.get('destinatario_razon_social'):
                raise ValidationError('Si el destinatario no es Consumidor Final, debe ingresar la Razon Social del mismo')
        else:
            data['destinatario_tenedor'] = 0
        if data['sujeto_generador'] in 'E':
            if not data['origen_cuit'] == data['cuit_empresa']:
                raise ValidationError('Si Sujeto Generador es Emisor, entonces Origen Cuit debe ser igual a Cuit Empresa')
        if data['transportista_cuit'] == data['cuit_empresa'] and not data['patente_vehiculo']:
            raise ValidationError('Si Transportista Cuit es igual a Cuit Empresa, debe ingresar Patente Vehiculo')
        
        if not data['importe'] and (data['producto_no_term_dev'] == 0 or data['origen_cuit'] != data['destinatario_cuit']):
            raise ValidationError('El valor del importe debe ser mayor a 0')
        return data
        
    def validate_cuit_empresa(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT de la Empresa no es valido")
        
    def validate_destinatario_cuit(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Destinatario no es valido")
        
    def validate_origen_cuit(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT de Origen no es valido")
        
    def validate_transportista_cuit(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Transportista no es valido")
        
    class Meta:
        model = COT
        exclude = ('file_path',)
        

class CTGSerializer(FriendlyErrorMessagesMixin, ModelSerializer):
    codigo_provincia_origen = serializers.CharField(source='codigo_localidad_origen.provincia.codigo')
    codigo_provincia_destino = serializers.CharField(source='codigo_localidad_destino.provincia.codigo')

    def validate_cuit_remitente(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Remitente no es valido")

    def validate_cuit_destino(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT de Destino no es valido")
        
    def validate_cuit_destinatario(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Destinatario no es valido")
        
    def validate_cuit_transportista(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Transportista no es valido")
        
    def validate_cuit_corredor(self, value):
        if not validar_cuit(value):
            raise ValidationError(u"El CUIT del Corredor no es valido")

    def create(self, validated_data):
        obj = CTG.objects.create(**validated_data)
        if validated_data.get('accion') == CTG_ACCION_SOLICITAR:
            obj.solicitar_ctg()
        return obj

    class Meta:
        model = CTG
        fields = '__all__'
    
        
class EntidadSerializer(FriendlyErrorMessagesMixin, ModelSerializer):

    class Meta:
        model = Entidad
        fields = ('usuario_solicitante', 'nombre', 'cuit',)


class CosechaSerializer(ModelSerializer):

    class Meta:
        model = Cosecha
        fields = ('codigo', 'descripcion',)
        
        
class EspecieSerializer(ModelSerializer):

    class Meta:
        model = Especie
        fields = ('codigo', 'descripcion',)
        
        
class EstablecimientoSerializer(ModelSerializer):

    class Meta:
        model = Establecimiento
        fields = ('codigo', 'descripcion',)
    
        
class CTGOperatiocionSerializer(ModelSerializer):

    class Meta:
        model = CTG
        fields = ('id', 'fecha', 'numero_carta_de_porte', 'numero_ctg',)
        

class COTOperatiocionSerializer(ModelSerializer):
    fecha = serializers.SerializerMethodField()
    
    def get_fecha(self, obj):
        return obtener_fecha_frontend(obj)
    
    class Meta:
        model = COT
        fields = ('id', 'fecha', 'tipo_comprobante', 'nro_comprobante', 'numero_comprobante')
