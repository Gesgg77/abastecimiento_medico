import django_filters
from .models import Insumo

class InsumoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio_caja", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio_caja", lookup_expr="lte")
    stock_min = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")

    class Meta:
        model = Insumo
        fields = ["categoria", "precio_min", "precio_max", "stock_min"]
