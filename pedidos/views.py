from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Carro, ItemCarro, Solicitud
from .permissions import EsGestor, EsInstitucion
from .serializers import (
    CambioEstadoSerializer,
    ItemCarroSerializer,
    SolicitudSerializer,
)
from .services import cambiar_estado_solicitud, confirmar_solicitud


class ItemCarroViewSet(viewsets.ModelViewSet):
    """CRUD del carro de la institución autenticada."""

    serializer_class = ItemCarroSerializer
    permission_classes = [EsInstitucion]
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]

    def get_queryset(self):
        carro, _ = Carro.objects.get_or_create(usuario=self.request.user)
        return carro.items.select_related("insumo", "insumo__categoria").all()

    def perform_create(self, serializer):
        carro, _ = Carro.objects.get_or_create(usuario=self.request.user)
        serializer.save(carro=carro)


class ConfirmarSolicitudView(APIView):
    permission_classes = [EsInstitucion]

    def post(self, request):
        solicitud = confirmar_solicitud(request.user)
        return Response(
            SolicitudSerializer(solicitud).data,
            status=status.HTTP_201_CREATED,
        )


class MisSolicitudesView(generics.ListAPIView):
    serializer_class = SolicitudSerializer
    permission_classes = [EsInstitucion]

    def get_queryset(self):
        return (
            Solicitud.objects.filter(institucion=self.request.user)
            .prefetch_related("detalles")
            .select_related("orden_despacho")
        )


class SolicitudesGestorView(generics.ListAPIView):
    serializer_class = SolicitudSerializer
    permission_classes = [EsGestor]
    queryset = (
        Solicitud.objects.all()
        .select_related("institucion")
        .prefetch_related("detalles")
    )


class CambiarEstadoSolicitudView(APIView):
    permission_classes = [EsGestor]

    def patch(self, request, pk):
        entrada = CambioEstadoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)

        solicitud = cambiar_estado_solicitud(
            solicitud_id=pk,
            nuevo_estado=entrada.validated_data["estado"],
        )
        return Response(SolicitudSerializer(solicitud).data)


def pagina_solicitudes(request):
    """
    Panel visual de demostración.
    Los datos NO se entregan desde esta vista: el navegador debe autenticarse
    con JWT y consumir los endpoints protegidos de la API.
    """
    return render(request, "pedidos/solicitudes.html")
