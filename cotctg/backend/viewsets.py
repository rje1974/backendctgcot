'''
Created on 6 sep. 2017

@author: Hugo Chavero
'''
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from backend.serializers import CTGSerializer, LocalidadSerializer
from backend.models import CTG, Localidad
from rest_framework.response import Response


class CTGViewSet(ModelViewSet):
    serializer_class = CTGSerializer
    
    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return CTG.objects.filter(usuario_solicitante=self.request.user)
        return []
    
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
        return ModelViewSet.create(self, request, *args, **kwargs)
    
class LocalidadViewSet(ReadOnlyModelViewSet):
    serializer_class = LocalidadSerializer
    queryset = Localidad.objects.all()[:5]