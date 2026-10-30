"""add content column to posts table

Revision ID: f71aa1bbd2d8
Revises: 460d500132b8
Create Date: 2026-10-28 20:38:51.724278

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision: str = 'f71aa1bbd2d8'
down_revision: Union[str, Sequence[str], None] = '460d500132b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", Column("content", String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
