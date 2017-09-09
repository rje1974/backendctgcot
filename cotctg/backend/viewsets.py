'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from backend.serializers import CTGSerializer, LocalidadSerializer,\
    EntidadSerializer, CosechaSerializer, EspecieSerializer,\
    EstablecimientoSerializer
from backend.models import CTG, Localidad, Entidad, Cosecha, Especie,\
    Establecimiento
from rest_framework.response import Response
from backend.constants import CTG_ESTADO_PENDIENTE, CTG_ESTADO_GENERADO


class CTGViewSet(ModelViewSet):
    serializer_class = CTGSerializer
    
    def get_queryset(self):
        return CTG.objects.filter(usuario_solicitante=self.request.user)
    
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
        request.data['usuario_solicitante'] = request.user.id
        response = ModelViewSet.create(self, request, *args, **kwargs)
        if response.data.get('estado') == CTG_ESTADO_PENDIENTE:
            return Response('CTG Creado parcialmente')
        elif response.data.get('estado') == CTG_ESTADO_GENERADO:
            import ipdb; ipdb.set_trace()
            return Response('CTG Creado Correctamente')
    
    
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
