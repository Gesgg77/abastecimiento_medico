# Abastecimiento Médico

Proyecto académico de **Desarrollo Backend** con Django REST Framework y PostgreSQL.

## Proyecto 5
Plataforma B2B para pedidos de fármacos e insumos médicos. Maneja dos roles:

- **INSTITUCION**: consulta catálogo, administra su carro persistente, confirma solicitudes y revisa su historial.
- **GESTOR**: administra categorías/insumos y cambia solicitudes PAGADAS a ENTREGADO o CANCELADO.

La solución no depende de `/admin/`. La gestión se realiza mediante endpoints REST y Swagger.

## Requisitos principales implementados

- PostgreSQL.
- Usuario personalizado con `CHOICES` de rol.
- JWT access + refresh con claim `rol`.
- CRUD de categorías e insumos.
- Filtros con django-filter y búsqueda.
- Carro persistente 1:1 con el usuario.
- CRUD de ítems del carro.
- Checkout transaccional con `transaction.atomic`.
- El stock NO baja al agregar al carro.
- El stock se valida y descuenta al pasar a PAGADO.
- Cancelar una solicitud repone el stock.
- Orden de despacho con UUID.
- Swagger/OpenAPI en `/api/docs/`.
- Vista base con footer de alumno, sección y año.

## Instalación rápida

### 1. Clonar y crear entorno

```powershell
git clone https://github.com/Gesgg77/abastecimiento_medico.git
cd abastecimiento_medico
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Crear archivo .env

Copia `.env.example` a `.env` y completa especialmente la contraseña de PostgreSQL y tu sección.

```powershell
Copy-Item .env.example .env
```

### 3. PostgreSQL

Ejemplo usado por el proyecto:

```sql
CREATE USER abastecimiento_user WITH PASSWORD 'TU_PASSWORD';
CREATE DATABASE abastecimiento_medico_db OWNER abastecimiento_user;
```

### 4. Crear tablas

```powershell
python manage.py makemigrations usuarios catalogo pedidos
python manage.py migrate
```

### 5. Crear Gestor de Bodega sin Django Admin

```powershell
python manage.py crear_gestor gestor gestor@farmacia.cl ClaveSegura123!
```

### 6. Ejecutar

```powershell
python manage.py runserver
```

Abrir:

- Inicio: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/api/docs/

## Endpoints principales

| Método | Endpoint | Acceso |
|---|---|---|
| POST | `/api/auth/registro/` | Público, crea INSTITUCION |
| POST | `/api/auth/token/` | Público |
| POST | `/api/auth/token/refresh/` | Público |
| GET | `/api/categorias/` | Público |
| POST/PUT/PATCH/DELETE | `/api/categorias/{id}/` | GESTOR |
| GET | `/api/insumos/` | Público |
| POST/PUT/PATCH/DELETE | `/api/insumos/{id}/` | GESTOR |
| GET/POST/PUT/PATCH/DELETE | `/api/carro-insumos/` | INSTITUCION |
| POST | `/api/solicitudes/confirmar/` | INSTITUCION |
| GET | `/api/mis-solicitudes/` | INSTITUCION |
| GET | `/api/solicitudes/` | GESTOR |
| PATCH | `/api/solicitudes/{id}/estado/` | GESTOR |

### Filtros de ejemplo

```text
/api/insumos/?categoria=1
/api/insumos/?precio_min=5000&precio_max=30000
/api/insumos/?stock_min=10
/api/insumos/?search=paracetamol
/api/insumos/?ordering=precio_caja
```

## Flujo central

```text
INSTITUCION
   ↓
CARRO persistente (1:1)
   ↓
ITEMS DEL CARRO
   ↓
POST /api/solicitudes/confirmar/
   ↓
PENDIENTE
   ↓ validación atómica de stock
PAGADO → descuenta stock + genera orden de despacho
   ↓
ENTREGADO
o
CANCELADO → repone stock
```

## Importante antes de entregar

Edita `.env`:

```text
STUDENT_NAME=Jorge Essus
STUDENT_SECTION=TU_SECCION
STUDENT_YEAR=2026
```

Reemplaza `TU_SECCION` por tu sección real. El archivo `.env` está ignorado por Git y no debe contenerse en el repositorio.
