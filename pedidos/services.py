from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from catalogo.models import Insumo
from .models import Carro, DetalleSolicitud, OrdenDespacho, Solicitud


@transaction.atomic
def confirmar_solicitud(usuario):
    """
    Checkout atómico:
    1) lee el carro persistente,
    2) bloquea los insumos,
    3) valida stock de todos,
    4) crea historial,
    5) descuenta stock solo al pagar,
    6) genera orden de despacho.
    """
    carro, _ = Carro.objects.get_or_create(usuario=usuario)
    items = list(carro.items.select_related("insumo").all())

    if not items:
        raise ValidationError("El carro está vacío.")

    insumos_bloqueados = {}
    for item in items:
        insumo = Insumo.objects.select_for_update().get(pk=item.insumo_id)
        if insumo.stock < item.cantidad:
            raise ValidationError(
                f"Stock insuficiente para {insumo.nombre_comercial}. "
                f"Disponible: {insumo.stock}."
            )
        insumos_bloqueados[item.insumo_id] = insumo

    solicitud = Solicitud.objects.create(
        institucion=usuario,
        estado=Solicitud.Estado.PENDIENTE,
    )

    total = Decimal("0.00")

    for item in items:
        insumo = insumos_bloqueados[item.insumo_id]
        subtotal = insumo.precio_caja * item.cantidad
        total += subtotal

        DetalleSolicitud.objects.create(
            solicitud=solicitud,
            insumo=insumo,
            nombre_insumo=insumo.nombre_comercial,
            lote=insumo.lote,
            cantidad=item.cantidad,
            precio_unitario=insumo.precio_caja,
            subtotal=subtotal,
        )

    # El stock NO se toca al agregar al carro. Se descuenta justo al pasar a PAGADO.
    for item in items:
        insumo = insumos_bloqueados[item.insumo_id]
        insumo.stock -= item.cantidad
        insumo.save(update_fields=["stock"])

    solicitud.total = total
    solicitud.estado = Solicitud.Estado.PAGADO
    solicitud.save(update_fields=["total", "estado", "actualizado_en"])

    OrdenDespacho.objects.create(solicitud=solicitud)

    # El carro sigue existiendo (1:1 con el usuario), pero queda vacío tras comprar.
    carro.items.all().delete()
    return solicitud


@transaction.atomic
def cambiar_estado_solicitud(solicitud_id, nuevo_estado):
    """Permite al Gestor entregar o cancelar una solicitud pagada."""

    solicitud = (
        Solicitud.objects.select_for_update()
        .prefetch_related("detalles")
        .get(pk=solicitud_id)
    )

    if solicitud.estado != Solicitud.Estado.PAGADO:
        raise ValidationError(
            f"Solo una solicitud PAGADA puede entregarse o cancelarse. "
            f"Estado actual: {solicitud.estado}."
        )

    if nuevo_estado == Solicitud.Estado.CANCELADO:
        # Se repone exactamente el stock que se descontó al pagar.
        for detalle in solicitud.detalles.all():
            insumo = Insumo.objects.select_for_update().get(pk=detalle.insumo_id)
            insumo.stock += detalle.cantidad
            insumo.save(update_fields=["stock"])

    solicitud.estado = nuevo_estado
    solicitud.save(update_fields=["estado", "actualizado_en"])
    return solicitud
