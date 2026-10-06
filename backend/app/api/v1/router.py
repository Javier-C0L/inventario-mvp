from fastapi import APIRouter

from app.api.v1 import categories, products, suppliers

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(categories.router)
api_router.include_router(suppliers.router)
api_router.include_router(products.router)
