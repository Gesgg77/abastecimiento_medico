from rest_framework import serializers
from .models import Categoria, Insumo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"

class InsumoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Insumo
        fields = (
            "id",
            "categoria",
            "categoria_nombre",
            "nombre_comercial",
            "principio_activo",
            "lote",
            "fecha_vencimiento",
            "precio_caja",
            "stock",
        )
