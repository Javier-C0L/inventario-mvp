from datetime import datetime

from sqlmodel import SQLModel


class SupplierCreate(SQLModel):
    name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class SupplierUpdate(SQLModel):
    name: str | None = None
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class SupplierRead(SQLModel):
    id: int
    name: str
    contact_name: str | None
    email: str | None
    phone: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime
