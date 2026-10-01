# Abastecimiento Médico

Proyecto académico de Desarrollo Backend con Django REST Framework y PostgreSQL.

## Descripción

Plataforma B2B para instituciones de salud y gestión de bodega farmacéutica.

Roles principales:

- INSTITUCION: consulta catálogo, administra su carro persistente, confirma solicitudes y revisa su historial.
- GESTOR: administra categorías e insumos y actualiza solicitudes a ENTREGADO o CANCELADO.

## Funcionalidades

- PostgreSQL.
- Usuario personalizado con roles mediante CHOICES.
- JWT con access y refresh, incluyendo claim de rol.
- CRUD de categorías e insumos.
- Filtros, búsqueda y ordenamiento.
- Carro persistente 1:1 con el usuario.
- Confirmación de solicitudes con transaction.atomic.
- Validación y descuento de stock al confirmar el pago.
- Reposición de stock al cancelar.
- Orden de despacho con UUID.
- Swagger / OpenAPI.
- Vistas HTML para presentación del sistema.

## Ejecución

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations usuarios catalogo pedidos
python manage.py migrate
python manage.py runserver
```

## PostgreSQL

Configurar en `.env`:

```text
DB_NAME=abastecimiento_medico_db
DB_USER=abastecimiento_user
DB_PASSWORD=TU_CLAVE
DB_HOST=localhost
DB_PORT=5432
```

## Usuario Gestor

```powershell
python manage.py crear_gestor gestor gestor@farmacia.cl Gestor12345!
```

## Rutas principales

- Inicio: `/`
- Catálogo visual: `/catalogo/insumos/`
- Categorías visuales: `/catalogo/categorias/`
- Panel de solicitudes: `/gestion/solicitudes/`
- Swagger: `/api/docs/`

## API principal

| Método | Endpoint | Acceso |
|---|---|---|
| POST | `/api/auth/registro/` | Público |
| POST | `/api/auth/token/` | Público |
| POST | `/api/auth/token/refresh/` | Público |
| GET | `/api/categorias/` | Público |
| POST | `/api/categorias/` | GESTOR |
| PUT/PATCH/DELETE | `/api/categorias/{id}/` | GESTOR |
| GET | `/api/insumos/` | Público |
| POST | `/api/insumos/` | GESTOR |
| PUT/PATCH/DELETE | `/api/insumos/{id}/` | GESTOR |
| GET/POST/PUT/PATCH/DELETE | `/api/carro-insumos/` | INSTITUCION |
| POST | `/api/solicitudes/confirmar/` | INSTITUCION |
| GET | `/api/mis-solicitudes/` | INSTITUCION |
| GET | `/api/solicitudes/` | GESTOR |
| PATCH | `/api/solicitudes/{id}/estado/` | GESTOR |

## Filtros de insumos

```text
/api/insumos/?categoria=1
/api/insumos/?precio_min=5000&precio_max=30000
/api/insumos/?stock_min=10
/api/insumos/?search=paracetamol
/api/insumos/?ordering=precio_caja
```

## Flujo de solicitud

```text
INSTITUCION
   ↓
CARRO PERSISTENTE
   ↓
CONFIRMAR SOLICITUD
   ↓
VALIDAR STOCK
   ↓
PAGADO → DESCUENTA STOCK + GENERA ORDEN DE DESPACHO
   ↓
ENTREGADO

o

CANCELADO → REPONE STOCK
```

El archivo `.env` no se incluye en el repositorio.
