# Product Backlog — MVP Inventario

Basado en `PLAN.md`. Priorización MoSCoW. Historias organizadas por épica e numeradas secuencialmente (US###).

> **Leyenda de prioridad:** **Must** = indispensable para el MVP · **Should** = necesaria pero no bloqueante · **Could** = valor añadido · **Won't (this MVP)** = fuera de alcance del MVP.

---

## Épica 1 — Fundación e Infraestructura

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US001 | Fundación | Como desarrollador, quiero levantar todo el entorno con Docker Compose para tener la app funcionando con un solo comando. | • `docker compose up --build` levanta `db`, `backend` y `frontend`.<br>• El contenedor `db` tiene healthcheck y volumen persistente.<br>• El backend aplica migraciones de Alembic al arrancar.<br>• `GET /health` responde `{"status":"ok"}`. | Must |
| US002 | Fundación | Como desarrollador, quiero que la configuración sea por variables de entorno para no hardcodear credenciales. | • `.env.example` documenta todas las variables.<br>• `DATABASE_URL`, `CORS_ORIGINS` y `VITE_API_URL` se leen del entorno.<br>• `.env` real está en `.gitignore`. | Must |
| US003 | Fundación | Como desarrollador, quiero CORS configurado en el backend para que el frontend en otro puerto pueda consumir la API en desarrollo. | • `CORS_ORIGINS` acepta lista de orígenes.<br>• Peticiones desde `http://localhost:5173` son aceptadas.<br>• Orígenes no listados son rechazados. | Must |
| US004 | Fundación | Como desarrollador, quiero que nginx proxyee `/api` al backend en producción para evitar problemas de CORS. | • `GET /api/v1/...` vía nginx responde correctamente.<br>• `GET /` sirve el build de React.<br>• SPA: rutas como `/productos` devuelven `index.html` (no 404). | Must |

## Épica 2 — Gestión de Productos

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US005 | Productos | Como usuario, quiero crear productos con toda su información para registrar lo que hay en el almacén. | • El formulario incluye: nombre, SKU, descripción, categoría, proveedor, cantidad, unidad, stock mínimo, precios, fechas, ubicación y estado.<br>• SKU y nombre son obligatorios; cantidades y precios no pueden ser negativos.<br>• `POST /api/v1/products` devuelve 201 con el producto creado.<br>• SKU duplicado devuelve error 400 con mensaje claro. | Must |
| US006 | Productos | Como usuario, quiero editar un producto para mantener su información actualizada. | • `PUT /api/v1/products/{id}` aplica solo campos enviados.<br>• Actualiza `updated_at`.<br>• Producto inexistente devuelve 404. | Must |
| US007 | Productos | Como usuario, quiero ver el detalle de un producto para consultarlo sin editarlo. | • Vista `/productos/:id` muestra todos los campos.<br>• Producto inexistente muestra mensaje de error amigable. | Must |
| US008 | Productos | Como usuario, quiero eliminar un producto con confirmación previa para borrar solo cuando esté seguro. | • Modal de confirmación muestra el nombre del producto.<br>• `DELETE /api/v1/products/{id}` devuelve 204 y desaparece del listado.<br>• Cancelar no produce cambios. | Must |
| US009 | Productos | Como usuario, quiero buscar productos por nombre o SKU para encontrarlos rápido. | • `GET /api/v1/products?search=texto` filtra con `ILIKE` en nombre y SKU.<br>• La búsqueda es insensible a mayúsculas.<br>• El listado se actualiza al pulsar "Buscar" o Enter. | Must |
| US010 | Productos | Como usuario, quiero filtrar productos por categoría y estado para acotar el listado. | • `?category_id=` y `?status=` funcionan individual y combinadamente.<br>• Los selects se cargan desde la API (categorías dinámicas). | Must |
| US011 | Productos | Como usuario, quiero paginación en el listado para manejar cientos de productos sin degradar la carga. | • Respuesta `{items, total, limit, offset}`.<br>• Botones Anterior/Siguiente con deshabilitamiento en extremos.<br>• Muestra "Página X de Y" y total.<br>• `limit` acotado entre 1 y 100 en la API. | Must |

## Épica 3 — Catálogos (Categorías y Proveedores)

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US012 | Catálogos | Como usuario, quiero crear/editar/eliminar categorías para organizar los productos. | • CRUD completo con nombre único.<br>• Nombre obligatorio; duplicado devuelve error 400.<br>• Confirmación antes de eliminar. | Must |
| US013 | Catálogos | Como usuario, quiero crear/editar/eliminar proveedores con sus datos de contacto. | • CRUD completo con nombre, contacto, email, teléfono y dirección.<br>• Nombre obligatorio y único.<br>• Confirmación antes de eliminar. | Must |

## Épica 4 — Control de Inventario (Movimientos)

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US014 | Movimientos | Como usuario, quiero registrar entradas de productos para sumar stock al recibir mercancía. | • `POST /api/v1/movements/in` incrementa la cantidad.<br>• Crea registro en `inventory_movements` con cantidad anterior/nueva.<br>• Cantidad debe ser > 0; producto inexistente devuelve 404. | Must |
| US015 | Movimientos | Como usuario, quiero registrar salidas de productos para descontar stock al vender o consumir. | • `POST /api/v1/movements/out` decrementa la cantidad.<br>• Si la salida supera el stock disponible, devuelve 400 "Stock insuficiente".<br>• El stock nunca queda negativo. | Must |
| US016 | Movimientos | Como usuario, quiero ver el historial de movimientos para auditar qué pasó con cada producto. | • `GET /api/v1/movements` paginado con filtros `product_id` y `movement_type`.<br>• Muestra fecha, producto, tipo (Entrada/Salida), cantidad, anterior y nuevo stock.<br>• Ordenado del más reciente al más antiguo. | Must |
| US017 | Movimientos | Como usuario, quiero que un producto con cantidad 0 se marque como "agotado" y vuelva a "vigente" al reponer. | • Al llegar a 0, `status = agotado`.<br>• Una entrada posterior lo devuelve a `vigente` automáticamente. | Must |
| US018 | Movimientos | Como usuario, quiero un indicador visual de "stock bajo" cuando la cantidad está en o bajo el mínimo. | • Cuando `quantity <= min_stock`, el listado muestra badge naranja "Stock bajo".<br>• El conteo de stock bajo aparece en el dashboard. | Must |

## Épica 5 — Control de Vencimientos

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US019 | Vencimientos | Como usuario, quiero que cada producto muestre su estado de vencimiento calculado para evaluar riesgo de un vistazo. | • `expiration_status` calculado: `vencido` (fecha < hoy), `proximo_a_vencer` (hoy ≤ fecha ≤ hoy + días configurados), `vigente` (posterior), `sin_fecha`.<br>• Se incluye en `ProductRead` de todos los endpoints de productos. | Must |
| US020 | Vencimientos | Como usuario, quiero ver colores verde/amarillo/rojo/gris para el estado de vencimiento. | • Verde = vigente, amarillo = próximo a vencer, rojo = vencido, gris = sin fecha.<br>• Badge visible en listado y detalle del producto. | Must |
| US021 | Vencimientos | Como usuario, quiero filtrar productos por estado de vencimiento para concentrarme en lo urgente. | • `?expiration=vencido\|proximo_a_vencer\|vigente\|sin_fecha` filtra en la API.<br>• El filtro está disponible en la UI junto a los demás. | Must |
| US022 | Vencimientos | Como administrador, quiero configurar cuántos días antes se considera "próximo a vencer". | • `GET/PUT /api/v1/settings` gestiona `expiration_warning_days` (0–365).<br>• Página Configuración persiste el valor.<br>• El cálculo de vencimientos usa el valor configurado (default 30). | Must |

## Épica 6 — Dashboard Principal

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US023 | Dashboard | Como usuario, quiero un panel inicial con indicadores clave para conocer el estado del inventario al abrir la app. | • `GET /api/v1/dashboard/summary` devuelve: total productos, unidades disponibles, stock bajo, próximos a vencer, vencidos y últimos 5 movimientos.<br>• Tarjetas KPI con colores distintos.<br>• La ruta `/` es el dashboard. | Must |

## Épica 7 — Interfaz de Usuario y UX

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US024 | UX | Como usuario, quiero una navegación clara con sidebar para moverme entre módulos. | • Sidebar con Dashboard, Productos, Movimientos, Categorías, Proveedores y Configuración.<br>• El ítem activo se resalta.<br>• En móvil la navegación sigue siendo accesible. | Must |
| US025 | UX | Como usuario, quiero ver estados de carga, error y vacío para entender qué pasa en cada momento. | • Spinner/texto "Cargando..." durante fetches.<br>• Mensajes de error rojos descriptivos.<br>• Mensaje "No hay productos/movimientos" en listas vacías. | Must |
| US026 | UX | Como usuario, quiero mensajes claros de éxito y error en cada operación. | • Confirmación verde tras crear/actualizar/eliminar.<br>• Errores del backend (400/404) se muestran con el `detail` del servidor.<br>• El interceptor de axios centraliza el manejo. | Must |
| US027 | UX | Como usuario, quiero formularios validados con mensajes descriptivos para no enviar datos incorrectos. | • Validación cliente: campos obligatorios, numéricos ≥ 0.<br>• Validación servidor vía Pydantic (422 con detalles).<br>• Los mensajes indican qué campo falla. | Must |
| US028 | UX | Como usuario, quiero un diseño responsive (escritorio, tablet, móvil) para usar la app desde cualquier dispositivo. | • Tablas con scroll horizontal en pantallas pequeñas.<br>• Formularios apilados en móvil y en cuadrícula en escritorio.<br>• KPI cards: 2 columnas en móvil, 5 en escritorio. | Must |
| US029 | UX | Como usuario, quiero tablas fáciles de leer con encabezados claros y filas diferenciadas. | • Encabezados con fondo gris y alineación izquierda.<br>• Filas separadas con bordes.<br>• Contenido legible a tamaños de fuente accesibles. | Should |

## Épica 8 — Habilitadores Técnicos

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US030 | Técnico | Como desarrollador, quiero una API REST versionada (`/api/v1`) con routers por módulo para mantener el código organizado. | • Prefijo `/api/v1` en todos los endpoints.<br>• Routers separados: products, categories, suppliers, movements, settings, dashboard.<br>• Documentación Swagger/OpenAPI en `/docs`. | Must |
| US031 | Técnico | Como desarrollador, quiero modelos SQLModel y esquemas Pydantic separados (Create/Read/Update) para validar datos sin exponer el ORM. | • Esquemas con restricciones (ge=0, longitudes máximas).<br>• `ProductRead` nunca expone campos internos no deseados.<br>• Validación automática con 422 en datos inválidos. | Must |
| US032 | Técnico | Como desarrollador, quiero migraciones con Alembic para evolucionar el esquema de forma trazable. | • Una revisión por cambio de esquema (0001–0004 actuales).<br>• `alembic upgrade head` es idempotente y se ejecuta al arrancar el backend.<br>• `downgrade` definido en cada revisión. | Must |
| US033 | Técnico | Como desarrollador, quiero el frontend con TypeScript estricto y un cliente API centralizado para evitar `any` y duplicidad. | • Interfaces en `types/`, cliente axios en `api/client.ts`.<br>• `npm run build` pasa `tsc --noEmit` sin errores.<br>• Interceptor de errores único. | Must |
| US034 | Técnico | Como desarrollador, quiero tests automatizados de las reglas de negocio (stock, vencimientos) para regresiones seguras. | • pytest: salida que excede stock falla; entrada incrementa; cálculo de `expiration_status` según días configurados.<br>• Tests ejecutables dentro del contenedor backend. | Should |
| US035 | Técnico | Como desarrollador, quiero un script de seed versionado para poblar datos de prueba de forma reproducible. | • Script SQL o Python que inserta categorías, proveedores y N productos con fechas variadas.<br>• Documentado en el README; compatible con `docker compose down -v`. | Could |

## Épica 9 — Autenticación (preparación para etapa posterior)

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US036 | Autenticación | Como administrador, quiero que exista la entidad `users` en el esquema para habilitar autenticación en la fase 2 sin migración grande. | • Tabla `users` (id, email, hashed_password, full_name, is_active, created_at) diseñada.<br>• No se expone login en el MVP. | Should |
| US037 | Autenticación | Como desarrollador, quiero un stub de dependencia `get_current_user` para inyectar auth después sin refactor masivo. | • Estructura de dependencias FastAPI lista para activarse.<br>• Endpoints actuales siguen funcionando sin auth. | Could |

## Won't have (this MVP)

| ID | Épica | Historia de Usuario | Criterios de Aceptación | Prioridad |
|---|---|---|---|---|
| US038 | Alcance | Como usuario, quiero reportes PDF/Excel del inventario — **no para el MVP**. | Pospuesto a fase posterior; no hay endpoint ni UI en el MVP. | Won't |
| US039 | Alcance | Como usuario, quiero importar productos desde CSV — **no para el MVP**. | Pospuesto; la carga es manual/individual en el MVP. | Won't |
| US040 | Alcance | Como usuario, quiero multi-almacén y traslados entre sedes — **no para el MVP**. | El modelo asume un único almacén (`location` dentro del almacén). | Won't |
| US041 | Alcance | Como usuario, quiero roles y permisos por usuario — **no para el MVP**. | La autenticación y autorización completa queda para la etapa posterior. | Won't |

---

## Preguntas de Clarificación

1. **Estado manual vs. calculado:** el plan define `status` del producto (vigente/próximo/vencido/agotado) como "derivado + manual". Hoy mantenemos `status` manual (solo se auto-cambia a `agotado`/`vigente` por movimientos) y `expiration_status` calculado. ¿Debe `status` calcularse completamente desde la fecha de vencimiento, ignorando el valor manual?
2. **Vencimiento sin cantidad:** ¿un producto agotado (quantity 0) debe seguir apareciendo en el dashboard de vencimientos o excluirse?
3. **Filtro de búsqueda:** el plan menciona búsqueda por "nombre, código o categoría". Hoy busca nombre y SKU; ¿debe también coincidir con el *nombre* de la categoría (requiere JOIN)?
4. **Unidades de medida:** ¿lista cerrada (unidad, kg, lb, L, ml, caja) o texto libre? Hoy es texto libre con default "unidad".
5. **Soft delete:** ¿eliminar productos es borrado físico (actual) o preferencia de borrado lógico (`is_active`) para conservar historial de movimientos?
6. **Vencimiento = día exacto:** ¿un producto que vence *hoy* es "próximo a vencer" (implementado hoy) o ya "vencido" a partir de la medianoche?
7. **Multiplicidad de imágenes:** el MVP usa `picsum.photos/seed/{id}` como placeholder. ¿En producción se subirá imagen real por producto (almacenamiento en disco/S3) o se mantienen placeholders?
8. **Auditoría de movimientos:** hoy el historial no registra quién hizo el movimiento. ¿Se requiere `user_id` en movimientos cuando entre la auth?
9. **Paginación del historial en el dashboard:** ¿5 movimientos es suficiente o debe ser configurable?
10. **Precios con impuestos:** ¿precio de venta debe incluir IVA o se muestra sin impuestos? Afecta solo presentación, no el MVP.
