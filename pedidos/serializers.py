from rest_framework import serializers

from .models import Carro, DetalleSolicitud, ItemCarro, OrdenDespacho, Solicitud


class ItemCarroSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(source="insumo.nombre_comercial", read_only=True)
    precio_caja = serializers.DecimalField(
        source="insumo.precio_caja",
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarro
        fields = ("id", "insumo", "insumo_nombre", "precio_caja", "cantidad", "subtotal")

    def get_subtotal(self, obj):
        return obj.insumo.precio_caja * obj.cantidad

    def validate_insumo(self, value):
        request = self.context.get("request")
        if request and self.instance is None:
            carro, _ = Carro.objects.get_or_create(usuario=request.user)
            if ItemCarro.objects.filter(carro=carro, insumo=value).exists():
                raise serializers.ValidationError(
                    "Este insumo ya está en el carro. Modifica su cantidad."
                )
        return value


class DetalleSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSolicitud
        fields = (
            "id",
            "insumo",
            "nombre_insumo",
            "lote",
            "cantidad",
            "precio_unitario",
            "subtotal",
        )


class OrdenDespachoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDespacho
        fields = ("codigo", "creada_en")


class SolicitudSerializer(serializers.ModelSerializer):
    institucion_nombre = serializers.CharField(source="institucion.username", read_only=True)
    detalles = DetalleSolicitudSerializer(many=True, read_only=True)
    orden_despacho = OrdenDespachoSerializer(read_only=True)

    class Meta:
        model = Solicitud
        fields = (
            "id",
            "institucion",
            "institucion_nombre",
            "estado",
            "total",
            "creado_en",
            "actualizado_en",
            "detalles",
            "orden_despacho",
        )
        read_only_fields = fields


class CambioEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(
        choices=[Solicitud.Estado.ENTREGADO, Solicitud.Estado.CANCELADO]
    )
