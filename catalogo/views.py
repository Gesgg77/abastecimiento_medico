from django.db.models import Count, Q, Sum
from django.shortcuts import render
from rest_framework import viewsets

from .filters import InsumoFilter
from .models import Categoria, Insumo
from .permissions import EsGestorOSoloLectura
from .serializers import CategoriaSerializer, InsumoSerializer


# -------------------------
# API REST
# -------------------------
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


# -------------------------
# Vistas HTML de presentación
# -------------------------
def pagina_insumos(request):
    """Catálogo visual para presentar los insumos sin exponer la Browsable API."""
    insumos = Insumo.objects.select_related("categoria").all()
    categorias = Categoria.objects.all()

    busqueda = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()

    if busqueda:
        insumos = insumos.filter(
            Q(nombre_comercial__icontains=busqueda)
            | Q(principio_activo__icontains=busqueda)
            | Q(lote__icontains=busqueda)
        )

    if categoria_id.isdigit():
        insumos = insumos.filter(categoria_id=int(categoria_id))

    contexto = {
        "insumos": insumos,
        "categorias": categorias,
        "busqueda": busqueda,
        "categoria_id": categoria_id,
        "total_insumos": Insumo.objects.count(),
        "stock_total": Insumo.objects.aggregate(total=Sum("stock"))["total"] or 0,
        "stock_bajo": Insumo.objects.filter(stock__lte=10).count(),
    }
    return render(request, "catalogo/insumos.html", contexto)


def pagina_categorias(request):
    """Resumen visual de categorías con cantidad de insumos y stock acumulado."""
    categorias = Categoria.objects.annotate(
        total_insumos=Count("insumos"),
        stock_total=Sum("insumos__stock"),
    ).order_by("nombre")

    return render(
        request,
        "catalogo/categorias.html",
        {
            "categorias": categorias,
            "total_categorias": Categoria.objects.count(),
            "total_insumos": Insumo.objects.count(),
        },
    )
