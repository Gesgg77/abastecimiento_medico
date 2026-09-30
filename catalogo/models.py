from django.db import models

class Categoria(models.Model):
    """Agrupa los insumos del catálogo médico."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    """Producto disponible en bodega, vendido por caja."""

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="insumos",
    )
    nombre_comercial = models.CharField(max_length=150)
    principio_activo = models.CharField(max_length=150, blank=True)
    lote = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    precio_caja = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nombre_comercial"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre_comercial", "lote"],
                name="insumo_nombre_lote_unico",
            )
        ]

    def __str__(self):
        return f"{self.nombre_comercial} - lote {self.lote}"
