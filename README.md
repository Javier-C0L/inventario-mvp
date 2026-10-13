# Inventario — MVP

Herramienta web para gestión de inventario. Ver `PLAN.md` para la arquitectura y fases.

## Stack
- Frontend: React 18 + TypeScript + Vite + Tailwind + nginx
- Backend: FastAPI + SQLModel + Alembic
- DB: PostgreSQL 16

## Levantar todo

```bash
cp .env.example .env   # ya incluido
docker compose up --build
```

- Frontend: http://localhost
- API docs (Swagger): http://localhost:8000/docs
- Health: http://localhost:8000/health

## Desarrollo local (sin Docker)

Backend:
```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
docker compose exec backend pytest
```

Cubren reglas de negocio: stock (nunca negativo, agotado/reactivación), cálculo de vencimientos, configuración, CRUD de productos y filtros. Usan SQLite en memoria, sin tocar la base de datos real.

## Datos de demostración (seed)

```bash
docker compose exec backend python -m scripts.seed 1000   # 1000 productos
docker compose exec backend python -m scripts.seed 25     # solo 25
```

El seed es idempotente: reutiliza categorías/proveedores existentes y no genera SKUs duplicados. Compatible con `docker compose down -v` (limpiar y volver a poblar).
