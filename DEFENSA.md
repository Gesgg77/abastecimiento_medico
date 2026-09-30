# Guía breve para la defensa

## 1. Arquitectura y PostgreSQL
**Pregunta:** ¿Por qué PostgreSQL y no SQLite?

**Idea que debes explicar:** La evaluación exige un motor real PostgreSQL/MySQL. Django se conecta mediante `django.db.backends.postgresql` y las credenciales se cargan desde variables de entorno.

**Relaciones principales:**
- Usuario 1:1 Carro.
- Carro 1:N ItemCarro.
- Categoría 1:N Insumo.
- Usuario 1:N Solicitud.
- Solicitud 1:N DetalleSolicitud.
- Solicitud 1:1 OrdenDespacho.

## 2. JWT y roles
El login entrega `access` y `refresh`. El access token incluye el claim `rol`, que puede ser `INSTITUCION` o `GESTOR`.

Los permisos de DRF deciden quién puede ejecutar cada endpoint.

## 3. Carro persistente
El carro no vive en la sesión del navegador. Está en PostgreSQL y tiene un `OneToOneField` con el usuario.

Por eso cerrar sesión o cambiar de dispositivo no elimina los ítems.

## 4. Stock y transacciones
Agregar un producto al carro **no descuenta stock**.

Al confirmar:
1. se abre `transaction.atomic`;
2. se bloquean los insumos con `select_for_update`;
3. se valida que todos tengan stock;
4. se crea la solicitud PENDIENTE;
5. se guarda el detalle histórico;
6. se descuenta stock;
7. la solicitud pasa a PAGADO;
8. se genera la orden de despacho;
9. se vacían los ítems del carro.

Si una parte falla, la transacción completa hace rollback.

## 5. Cancelación
Solo una solicitud PAGADA puede cancelarse. Al cancelar, se recorre cada detalle y se devuelve al inventario la cantidad originalmente descontada.

## 6. Precio histórico
`DetalleSolicitud` guarda `precio_unitario`, `subtotal`, nombre y lote. Por eso un cambio futuro en el catálogo no modifica la compra histórica.

## 7. Filtros y Swagger
`django-filter` permite filtrar categoría, precio y stock. DRF SearchFilter permite buscar por nombre, principio activo o lote.

`drf-spectacular` genera OpenAPI y Swagger en `/api/docs/`.

## Preguntas que debes poder responder sin mirar
1. ¿Qué diferencia hay entre `makemigrations` y `migrate`?
2. ¿Qué significa una relación 1:1?
3. ¿Por qué el carro está en la base de datos?
4. ¿Por qué no se descuenta stock al agregar al carro?
5. ¿Para qué sirve `transaction.atomic`?
6. ¿Qué evita `select_for_update`?
7. ¿Qué diferencia hay entre INSTITUCION y GESTOR?
8. ¿Qué hace un serializer?
9. ¿Qué hace un ViewSet?
10. ¿Por qué una solicitud pagada no se elimina como un registro cualquiera?
