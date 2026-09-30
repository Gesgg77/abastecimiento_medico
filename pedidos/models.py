import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from catalogo.models import Insumo


class Carro(models.Model):
    """Carro activo persistente: relación 1 a 1 con el usuario."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carro",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carro de {self.usuario.username}"


class ItemCarro(models.Model):
    """Cada fila representa un insumo y su cantidad de cajas en el carro."""

    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="items")
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["carro", "insumo"],
                name="item_unico_por_carro",
            )
        ]

    def __str__(self):
        return f"{self.insumo.nombre_comercial} x {self.cantidad}"


class Solicitud(models.Model):
    """Registro histórico de la compra realizada por una institución."""

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PAGADO = "PAGADO", "Pagado"
        ENTREGADO = "ENTREGADO", "Entregado"
        CANCELADO = "CANCELADO", "Cancelado"

    institucion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="solicitudes",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.estado}"


class DetalleSolicitud(models.Model):
    """Congela precio y datos del insumo al momento de comprar."""

    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    nombre_insumo = models.CharField(max_length=150)
    lote = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"Detalle solicitud #{self.solicitud_id}: {self.nombre_insumo}"


class OrdenDespacho(models.Model):
    """Orden generada automáticamente cuando la solicitud queda PAGADA."""

    solicitud = models.OneToOneField(
        Solicitud,
        on_delete=models.CASCADE,
        related_name="orden_despacho",
    )
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Despacho {self.codigo}"
