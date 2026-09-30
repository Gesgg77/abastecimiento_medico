from rest_framework import viewsets

from .filters import InsumoFilter
from .models import Categoria, Insumo
from .permissions import EsGestorOSoloLectura
from .serializers import CategoriaSerializer, InsumoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsGestorOSoloLectura]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre"]

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.select_related("categoria").all()
    serializer_class = InsumoSerializer
    permission_classes = [EsGestorOSoloLectura]
    filterset_class = InsumoFilter
    search_fields = ["nombre_comercial", "principio_activo", "lote"]
    ordering_fields = ["nombre_comercial", "precio_caja", "stock", "fecha_vencimiento"]
