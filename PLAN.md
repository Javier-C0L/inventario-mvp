# Plan de Desarrollo — MVP Inventario

## 1. Arquitectura propuesta

```
┌─────────────┐      HTTP/JSON      ┌─────────────┐            ┌──────────────┐
│   React     │  ←───────────────→  │   FastAPI   │ ←────────→ │  PostgreSQL  │
│  (Vite+TS)  │   fetch/axios REST  │   (Pydantic)│  SQLModel  │              │
│  Tailwind   │                     │  SQLModel   │  SQLAlchemy│              │
│   nginx     │                     │   Alembic   │            │              │
└─────────────┘                     └─────────────┘            └──────────────┘
   :5173/80                              :8000                       :5432
```

- **Frontend**: SPA en React 18 + TypeScript + Vite, Tailwind, React Router, TanStack Query (o fetch simple para MVP), servidor nginx con build de producción.
- **Backend**: FastAPI con SQLModel, módulos por dominio (`products`, `categories`, `suppliers`, `movements`), esquemas Pydantic separados de tablas, paginación con `limit/offset`, CORS habilitado, `/docs` de Swagger incluido.
- **DB**: PostgreSQL 16, migraciones con Alembic, tabla `users` mínima preparada para futura auth.
- **Orquestación**: `docker-compose.yml` con 3 servicios + volumen para postgres + healthchecks. Variables por `.env`.

## 2. Diseño de base de datos

```
categories (id, name, description, created_at, updated_at)
suppliers  (id, name, contact_email, phone, address, ...)
products   (id, sku, name, description, category_id→categories, supplier_id→suppliers,
            quantity, unit, min_stock, purchase_price, sale_price,
            entry_date, expiration_date, location, status,
            created_at, updated_at)
inventory_movements (id, product_id→products, movement_type [IN/OUT],
                     quantity, previous_quantity, new_quantity, note, created_at)
users      (id, email, hashed_password, full_name, is_active, created_at)  -- futuro
app_settings (key, value)  -- p.ej. "expiration_warning_days" = 30
```

**Relaciones**: `products.category_id → categories.id` (N:1), `products.supplier_id → suppliers.id` (N:1), `inventory_movements.product_id → products.id` (N:1).

**Reglas de negocio en el backend** (no en la BD):
- Salida (`OUT`) falla si `quantity > stock actual` → evita negativos.
- `status` derivado + manual: `vigente | próximo_a_vencer | vencido | agotado`. Se calcula: vencido si `expiration_date < hoy`, próximo si `< hoy + warning_days` configurado en `app_settings`.
- Alerta de stock bajo: `quantity <= min_stock`.

## 3. Endpoints principales (REST)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/products` | Lista con búsqueda (`?search=`), filtros (`?category_id=&status=&expiration_status=`), paginación (`?limit=&offset=`) |
| POST | `/api/v1/products` | Crear |
| GET | `/api/v1/products/{id}` | Detalle |
| PUT/PATCH | `/api/v1/products/{id}` | Editar |
| DELETE | `/api/v1/products/{id}` | Eliminar |
| GET | `/api/v1/categories` · POST/PUT/DELETE `/{id}` | CRUD categorías |
| GET | `/api/v1/suppliers` · POST/PUT/DELETE `/{id}` | CRUD proveedores |
| POST | `/api/v1/movements/in` | Registrar entrada `{product_id, quantity, note}` |
| POST | `/api/v1/movements/out` | Registrar salida (valida stock) |
| GET | `/api/v1/movements` | Historial con filtros `?product_id=&type=` |
| GET | `/api/v1/dashboard/summary` | Totales: productos, unidades, stock bajo, próximos, vencidos, últimos movimientos |
| GET/PUT | `/api/v1/settings` | Leer/actualizar `expiration_warning_days` |

Errores consistentes: `{detail: "..."}` con códigos 400/404/422. Respuestas paginadas: `{items: [], total, limit, offset}`.

## 4. Estructura de carpetas

**Backend** `backend/`:
```
app/
  main.py               # create_app, CORS, routers, /health
  core/config.py        # Settings (pydantic-settings)
  db/session.py, base.py
  migrations/           # Alembic
  models/               # tablas SQLModel (product.py, category.py, supplier.py, movement.py, user.py)
  schemas/              # Pydantic request/response (product.py, ...)
  api/v1/
    products.py, categories.py, suppliers.py, movements.py, dashboard.py, settings.py
  services/             # lógica: movement_service (valida stock, error si negativo), product_service
  tests/
requirements.txt  (o pyproject.toml)
Dockerfile
alembic.ini
```

**Frontend** `frontend/`:
```
src/
  main.tsx, App.tsx, routes.tsx
  api/client.ts         # axios/fetch baseURL, interceptors error
  api/products.ts, dashboard.ts, movements.ts, settings.ts
  types/index.ts        # Product, Category, Supplier, Movement, DashboardSummary
  pages/
    DashboardPage.tsx, ProductsPage.tsx, ProductFormPage.tsx,
    MovementsPage.tsx, SettingsPage.tsx, CategoriesPage.tsx, SuppliersPage.tsx
  components/
    table/DataTable.tsx, layout/Sidebar.tsx + Header.tsx,
    ui/Button.tsx, Modal.tsx, Badge.tsx (verde/amarillo/rojo),
    forms/ProductForm.tsx, MovementForm.tsx, FiltersBar.tsx, Pagination.tsx
  hooks/useProducts.ts  # estado carga/error/vacío
Dockerfile, nginx.conf, vite.config.ts, tailwind.config.js
```

## 5. Flujo de navegación

- `/` → Dashboard (KPIs + últimas movimientos + alertas)
- `/productos` → tabla con buscador, filtros, paginación → `/productos/nuevo` | `/productos/:id` (detalle) | `/productos/:id/editar`
- `/movimientos` → historial + botones "Entrada"/"Salida" (modal)
- `/categorias`, `/proveedores` → CRUD simple en tabla+modal
- `/configuracion` → días de aviso de vencimiento, umbrales

Confirmaciones con modal antes de eliminar; toasts para éxito/error.

## 6. Fases priorizadas

**Fase 0 — Base (setup)**: docker-compose con postgres + backend + frontend; Alembic inicial; salud `/health`; CORS; `.env.example`.

**Fase 1 — Catálogos + Productos (core)**: modelos Category/Supplier/Product, CRUD completo, schemas Pydantic, búsqueda y filtros, paginación, tabla UI + formulario validado.

**Fase 2 — Movimientos + reglas**: IN/OUT con actualización atómica de stock, validación anti-negativos, historial, alertas stock bajo en dashboard.

**Fase 3 — Vencimientos**: cálculo de estado (vigente/próximo/vencido), configuración de días, badges de color, filtro por estado, sección "próximos a vencer".

**Fase 4 — Dashboard + pulido UX**: endpoint summary, estados de carga/vacío/error, modales de confirmación, toasts, responsive (tabla → cards en móvil), paginación completa.

**Fase 5 — Hardening MVP**: tests mínimos (pytest en reglas de stock/vencimiento, RTL en formularios), manejo de errores global, seed de datos demo, README, ajustes de producción (nginx gzip, variables).

*No incluido en MVP*: auth real, roles, reportes PDF, multi-almacén, importación CSV — solo dejando `users` + config lista para fase posterior.

## 7. Ejemplos rápidos

**Modelo SQLModel (backend)**:
```python
class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True)
    name: str
    quantity: int = Field(ge=0, default=0)
    min_stock: int = Field(ge=0, default=0)
    expiration_date: date | None = None
    category_id: int | None = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
```

**Esquema + endpoint**:
```python
class ProductCreate(SQLModel):
    sku: str; name: str; quantity: int >= 0; min_stock: int = 0
    expiration_date: date | None = None

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    ...
```

**Movimiento (regla de stock)**:
```python
def register_movement(product_id, type, quantity, session):
    product = session.get(Product, product_id)
    if type == MovementType.OUT and quantity > product.quantity:
        raise HTTPException(400, "Stock insuficiente: no se permiten cantidades negativas")
    product.quantity += quantity if type == MovementType.IN else -quantity
    movement = InventoryMovement(..., previous_quantity=..., new_quantity=product.quantity)
    session.add(movement); session.commit()
```

**Componente frontend**:
```tsx
// components/ui/ExpirationBadge.tsx
export function expirationColor(date: string|null, warningDays: number) {
  if (!date) return "gray";
  const days = differenceInDays(parseISO(date), new Date());
  if (days < 0) return "red";      // vencido
  if (days <= warningDays) return "yellow"; // próximo
  return "green";
}
```

```tsx
// api/client.ts — centralizado, sin any
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL });
export async function getProducts(params: ProductQuery): Promise<Paginated<Product>> { ... }
```

## 8. Containerización

**`docker-compose.yml`** (servicios):
```yaml
services:
  db:
    image: postgres:16-alpine
    environment: POSTGRES_USER/PASSWORD/DB
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: pg_isready
  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    env_file: .env
    depends_on: db: {condition: service_healthy}
    # también: alembic upgrade head && uvicorn ...
  frontend:
    build: ./frontend   # multi-stage node:build → nginx
    ports: ["80:80"]
    depends_on: [backend]
```

**Backend Dockerfile**: `python:3.12-slim`, instalar deps, copiar `app/`, CMD `alembic upgrade head && uvicorn`.

**Frontend Dockerfile**: etapa `node:20-alpine` → `npm ci && npm run build`; etapa final `nginx:alpine` copiando `dist/` + `nginx.conf` con proxy `/api → backend:8000` (evita CORS en prod).

## 9. Recomendaciones para mantenerlo simple y escalable

1. **Reglas de negocio en `services/`**, no en endpoints ni en el frontend: el frontend solo muestra.
2. **Un solo cliente API** (`api/client.ts`) con tipos compartidos; evita `any`, define `Paginated<T>` genérico.
3. **Schemas separados** de tablas (`ProductCreate/Read/Update`) — no exponer modelos ORM.
4. **Enums para estados y tipos de movimiento** en BD y en TS.
5. **Paginación y filtros server-side desde el día 1**; no cargar todos los productos.
6. **Migraciones con Alembic** aunque duela al inicio; en MVP evita `create_all` en prod.
7. **Componentes UI pequeños** (`Badge`, `Modal`, `DataTable`) reutilizables; páginas solo orquestan.
8. **Toasts + confirmaciones** para todas las acciones destructivas o de error.
9. **Tests mínimos enfocados**: reglas de stock y cálculo de vencimiento (mayor valor de negocio), no cobertura total.
10. **`.env.example` + README** con comandos `docker compose up`; configuración por variables, nada hardcodeado.
11. **No agregar auth en MVP**, pero dejar `users` y dependency `get_current_user` como stub para la fase 2.
