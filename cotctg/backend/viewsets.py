'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from backend.serializers import CTGSerializer, LocalidadSerializer,\
    EntidadSerializer, CosechaSerializer, EspecieSerializer,\
    EstablecimientoSerializer, CTGOperatiocionSerializer,\
    COTOperatiocionSerializer, COTSerializer
from backend.models import CTG, Localidad, Entidad, Cosecha, Especie,\
    Establecimiento, COT
from rest_framework.response import Response
from backend.constants import CTG_ESTADO_PENDIENTE


class COTViewSet(ModelViewSet):
    serializer_class = COTSerializer

    def get_queryset(self):
        queryset = COT.objects.filter(usuario_solicitante=self.request.user)
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def create(self, request, *args, **kwargs):
        print request.data
        request.data['usuario_solicitante'] = request.user.id
        return ModelViewSet.create(self, request, *args, **kwargs)

    
class CTGViewSet(ModelViewSet):
    serializer_class = CTGSerializer
    
    def get_queryset(self):
        queryset = CTG.objects.filter(usuario_solicitante=self.request.user)
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            queryset = queryset.filter(id=item_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        # TODO: Anular CTG
        obj = CTG.objects.get(pk=kwargs['pk'])
        obj.anular_ctg()
        codigo_operacion = obj.codigo_operacion 
        if codigo_operacion:
            return Response('CTG Anulado correctamente: codigo operacion {}.'.format(codigo_operacion))
        else:
            return Response('CTG Parcial Anulado.')
    
    def create(self, request, *args, **kwargs):
        print request.data
        request.data['usuario_solicitante'] = request.user.id
        request.data['estado'] = CTG_ESTADO_PENDIENTE
        
        '''
        if self._check_required_fields(request.data):
            # Guardo y genero CTG
            
            especie_obj = Especie.objects.get(codigo=request.data['codigo_especie'])
            cosecha_obj = Cosecha.objects.get(codigo=request.data['codigo_cosecha'])
            destino_obj, destino_obj_created = Entidad.objects.get_or_create(cuit=request.data['cuit_destino'])
            destinatario_obj, destinatario_obj_created = Entidad.objects.get_or_create(cuit=request.data['cuit_destinatario'])
            localidad_origen_obj = Localidad.objects.get(codigo=request.data['codigo_localidad_origen'])
            localidad_destino_obj = Localidad.objects.get(codigo=request.data['codigo_localidad_destino'])
            transportista_obj, transportista_obj_created = Entidad.objects.get_or_create(cuit=request.data['cuit_transportista'])
            
            request.data['codigo_especie'] = especie_obj.id
            request.data['cuit_destino'] = destino_obj.id
            request.data['cuit_destinatario'] = destinatario_obj.id
            request.data['cuit_transportista'] = transportista_obj.id
            request.data['codigo_cosecha'] = cosecha_obj.id
            request.data['codigo_localidad_origen'] = localidad_origen_obj.id
            request.data['codigo_localidad_destino']= localidad_destino_obj.id
            
        if request.data['cuit_remitente']:
            remitente_obj, remitente_obj_created = Entidad.objects.get_or_create(cuit=request.data['cuit_remitente'])
            request.data['cuit_remitente'] = remitente_obj.id 
        '''
        return super(CTGViewSet, self).create(request, *args, **kwargs)
        '''
        response = super(CTGViewSet, self).create(request, *args, **kwargs)
        if response.data.get('estado') == CTG_ESTADO_GENERADO:
            resp = {}
            resp['title'] = 'CTG Creado Correctamente'
            resp['numero_ctg'] = response.data.get('numero_ctg')
            resp['fechahora'] = response.data.get('fechahora')
            resp['vigenciadesde'] = response.data.get('vigenciadesde')
            resp['vigenciahasta'] = response.data.get('vigenciahasta')
            resp['tarifareferencia'] = response.data.get('tarifareferencia')
            return Response(resp)
        return Response('CTG Creado parcialmente')
        '''
    
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
        r_fields['peso_neto_carga'] = post_fields.get('peso_neto_carga')
        r_fields['km_a_recorrer'] = post_fields.get('km_a_recorrer')
        r_fields['patente_vehiculo'] = post_fields.get('patente_vehiculo')
        
        for value in r_fields.itervalues():
            if not value: return False
        return True
    
    
class EntidadViewSet(ModelViewSet):
    serializer_class = EntidadSerializer
    
    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Entidad.objects.filter(usuario_solicitante=self.request.user)
        return []
    
    def create(self, request, *args, **kwargs):
        request.data['usuario_solicitante'] = request.user.id
        return ModelViewSet.create(self, request, *args, **kwargs)


class LocalidadViewSet(ReadOnlyModelViewSet):
    serializer_class = LocalidadSerializer
    queryset = Localidad.objects.all()[:30]
    

class CosechaViewSet(ReadOnlyModelViewSet):
    serializer_class = CosechaSerializer
    queryset = Cosecha.objects.all()


class EspecieViewSet(ReadOnlyModelViewSet):
    serializer_class = EspecieSerializer
    queryset = Especie.objects.all()


class EstablecimientoViewSet(ReadOnlyModelViewSet):
    serializer_class = EstablecimientoSerializer
    queryset = Establecimiento.objects.all()


class OperacionViewSet(ReadOnlyModelViewSet):
        
    def list(self, request):
        resp_list = []
        # TODO: Recibir parametro para efectuar filtro en consulta
        
        #ctg_queryset = CTG.objects.filter(estado=CTG_ESTADO_GENERADO)
        ctg_queryset = CTG.objects.all()
        cot_queryset = COT.objects.all()
        serializer_ctg = CTGOperatiocionSerializer(ctg_queryset, many=True).data
        serializer_cot = COTOperatiocionSerializer(COT.objects.all(), many=True).data
        if serializer_cot:
            resp_obj = {}
            resp_obj['title'] = 'COTs'
            resp_obj['data'] = serializer_cot
            resp_list.append(resp_obj) 
        if serializer_ctg:
            resp_obj = {}
            resp_obj['title'] = 'CTGs'
            resp_obj['data'] = serializer_ctg
            resp_list.append(resp_obj)
        
        return Response(resp_list)
    
