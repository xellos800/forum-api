"""add last columns to posts table

Revision ID: 350619c8b600
Revises: 30e1c1b63ff7
Create Date: 2026-10-29 10:53:55.260285

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, Column, String, TIMESTAMP, BOOLEAN
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '350619c8b600'
down_revision: Union[str, Sequence[str], None] = '30e1c1b63ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",
                  Column("published", BOOLEAN, server_default="TRUE"))
    op.add_column("posts",
                  Column("created_at", TIMESTAMP(timezone=True),
                         server_default=func.current_timestamp(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
