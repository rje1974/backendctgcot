'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.serializers import ModelSerializer
from backend.models import Localidad, Provincia, CTG, Entidad, Cosecha, Especie,\
    Establecimiento
from backend.constants import CTG_ESTADO_PENDIENTE


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
        
class CTGSerializer(ModelSerializer):
    class Meta:
        model = CTG
        fields = '__all__'

    def create(self, validated_data):
        validated_data['estado'] = CTG_ESTADO_PENDIENTE
        has_required_fields = self._check_required_fields(validated_data)
        obj = CTG.objects.create(**validated_data)
        print validated_data
        remitente = validated_data.get('cuit_remitente')
        if remitente:
            remitente_obj = Entidad.objects.get_or_create(cuit=remitente)
            obj.cuit_remitente.add(remitente_obj)
        
        
        
        if has_required_fields:
            # Guardo y genero CTG
            especie_obj = Especie.objects.get(codigo=validated_data['codigo_especie'])
            destino_obj = Entidad.objects.get_or_create(cuit=validated_data['cuit_destino'])
            destinatario_obj = Entidad.objects.get_or_create(cuit=validated_data['cuit_destinatario'])
            cosecha_obj = Cosecha.objects.get(codigo=validated_data['codigo_cosecha'])
            localidad_origen_obj = Localidad.objects.get(codigo=validated_data['codigo_localidad_origen'])
            localidad_destino_obj = Localidad.objects.get(codigo=validated_data['codigo_localidad_destino'])
            
            obj.especie.add(especie_obj)
            obj.cuit_destino.add(destino_obj)
            obj.cuit_destinatario.add(destinatario_obj)
            obj.codigo_cosecha.add(cosecha_obj)
            obj.codigo_localidad_origen.add(localidad_origen_obj)
            obj.codigo_localidad_destino.add(localidad_destino_obj)
            obj.solicitar_ctg()
        return obj
        
    def _check_required_fields(self, data):
        post_fields = data
        # Genero un nuevo dict con todos los campos requeridos
        r_fields = {}
        r_fields['codigo_especie'] = post_fields.get('codigo_especie')
        r_fields['cuit_destino'] = post_fields.get('cuit_destino')
        r_fields['cuit_destinatario'] = post_fields.get('cuit_destinatario')
        r_fields['codigo_cosecha'] = post_fields.get('codigo_cosecha')
        r_fields['codigo_localidad_origen'] = post_fields.get('codigo_localidad_origen')
        r_fields['codigo_localidad_destino'] = post_fields.get('codigo_localidad_destino')
        r_fields['numero_carta_de_porte'] = post_fields.get('numero_carta_de_porte')
        r_fields['estado'] = post_fields.get('estado')
        r_fields['peso_neto_carga'] = post_fields.get('peso_neto_carga')
        r_fields['km_a_recorrer'] = post_fields.get('km_a_recorrer')
        r_fields['patente_vehiculo'] = post_fields.get('patente_vehiculo')
        
        for value in r_fields.itervalues():
            if not value: return False
        return True

        
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