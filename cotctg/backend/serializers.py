'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.serializers import ModelSerializer
from backend.models import Localidad, Provincia, CTG, Entidad, Cosecha, Especie,\
    Establecimiento, COT
from backend.constants import CTG_ACCION_SOLICITAR, COT_ACCION_SOLICTAR


class ProvinciaSerializer(ModelSerializer):
    class Meta:
        model= Provincia
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


class COTSerializer(ModelSerializer):
    class Meta:
        model = COT
        fields = '__all__'

    def create(self, validated_data):
        obj = COT.objects.create(**validated_data)
        if validated_data.get('generar_cot'):
            obj.solicitar_cot()
        return obj
        
        
class CTGSerializer(ModelSerializer):
    class Meta:
        model = CTG
        fields = '__all__'
        #exclude = ('usuario_solicitante',)
        #depth = 2

    def create(self, validated_data):
        obj = CTG.objects.create(**validated_data)
        if validated_data.get('accion') == CTG_ACCION_SOLICITAR:
            obj.solicitar_ctg()
        return obj
    
        
class EntidadSerializer(ModelSerializer):
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
    class Meta:
        model = COT
        fields = ('id', 'fecha',)