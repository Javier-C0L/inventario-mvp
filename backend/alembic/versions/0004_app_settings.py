"""app settings

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-06

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_setting",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sqlmodel.sql.sqltypes.AutoString(length=80), nullable=False),
        sa.Column("value", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_app_setting_key", "app_setting", ["key"], unique=True)
    op.execute("INSERT INTO app_setting (key, value) VALUES ('expiration_warning_days', '30')")


def downgrade() -> None:
    op.drop_table("app_setting")
