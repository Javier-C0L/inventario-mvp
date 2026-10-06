from datetime import date, datetime

from pydantic import Field
from sqlmodel import SQLModel

from app.models.product import ProductStatus


class ProductCreate(SQLModel):
    sku: str
    name: str
    description: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    quantity: int = 0
    unit: str = "unidad"
    min_stock: int = 0
    purchase_price: float = 0
    sale_price: float = 0
    entry_date: date = Field(default_factory=date.today)
    expiration_date: date | None = None
    location: str | None = None
    status: ProductStatus = ProductStatus.vigente


class ProductUpdate(SQLModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    quantity: int | None = None
    unit: str | None = None
    min_stock: int | None = None
    purchase_price: float | None = None
    sale_price: float | None = None
    entry_date: date | None = None
    expiration_date: date | None = None
    location: str | None = None
    status: ProductStatus | None = None


class ProductRead(SQLModel):
    id: int
    sku: str
    name: str
    description: str | None
    category_id: int | None
    supplier_id: int | None
    quantity: int
    unit: str
    min_stock: int
    purchase_price: float
    sale_price: float
    entry_date: date
    expiration_date: date | None
    location: str | None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    expiration_status: str = "sin_fecha"


class ProductList(SQLModel):
    items: list[ProductRead]
    total: int
    limit: int
    offset: int
