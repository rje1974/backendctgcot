'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.serializers import ModelSerializer
from backend.models import Localidad, Provincia, CTG, Entidad


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
        
        
class CTGSerializer(ModelSerializer):
    class Meta:
        model = CTG
        fields = '__all__'
    '''      
    def create(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        request.data['usuario_solicitante'] = request.user.id
        request.data['estado'] = 3
        has_required_fields = self._check_required_fields(request)
        
        if has_required_fields:
            # Guardo y genero CTG
            #obj.solicitar_ctg()
            request.data['estado'] = 2
        return super(CTGSerializer, self).create(request, *args, **kwargs)
    '''
    def create(self, validated_data):
        validated_data['estado'] = 3
        has_required_fields = self._check_required_fields(validated_data)
        obj = CTG.objects.create(**validated_data)
        if has_required_fields:
            # Guardo y genero CTG
            obj.solicitar_ctg()
            obj.estado = 2
        return obj
        
    def _check_required_fields(self, data):
        post_fields = data
        # Genero un nuevo dict con todos los campos requeridos
        r_fields = {}
        r_fields['codigo_especie'] = post_fields.get('codigo_especie')
        r_fields['cuit_destino'] = post_fields.get('cuit_destino')
        r_fields['cuit_destinatario'] = post_fields.get('cuit_destinatario')
        r_fields['cuit_cosecha'] = post_fields.get('cuit_cosecha')
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
