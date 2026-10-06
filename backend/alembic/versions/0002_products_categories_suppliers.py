"""products categories suppliers

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-06

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=120), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_category_name", "category", ["name"])
    op.create_table(
        "supplier",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=120), nullable=False),
        sa.Column("contact_name", sqlmodel.sql.sqltypes.AutoString(length=120), nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(length=120), nullable=True),
        sa.Column("phone", sqlmodel.sql.sqltypes.AutoString(length=40), nullable=True),
        sa.Column("address", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_supplier_name", "supplier", ["name"])
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sqlmodel.sql.sqltypes.AutoString(length=60), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=160), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("supplier_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit", sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
        sa.Column("min_stock", sa.Integer(), nullable=False),
        sa.Column("purchase_price", sa.Float(), nullable=False),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        sa.Column("location", sqlmodel.sql.sqltypes.AutoString(length=120), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["supplier.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_product_sku", "product", ["sku"], unique=True)
    op.create_index("ix_product_name", "product", ["name"])


def downgrade() -> None:
    op.drop_table("product")
    op.drop_table("supplier")
    op.drop_table("category")
