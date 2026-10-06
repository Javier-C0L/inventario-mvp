from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel

from app.models.base import utcnow


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"


class InventoryMovement(SQLModel, table=True):
    __tablename__ = "inventory_movement"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    movement_type: str = Field(max_length=3)
    quantity: int = Field(gt=0)
    previous_quantity: int
    new_quantity: int
    note: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=utcnow)
