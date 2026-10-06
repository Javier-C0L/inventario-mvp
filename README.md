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
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```
