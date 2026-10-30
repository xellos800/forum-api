"""add fkey posts table

Revision ID: 30e1c1b63ff7
Revises: 7611a4f9c6cc
Create Date: 2026-10-28 21:16:13.370578

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, Column, String, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '30e1c1b63ff7'
down_revision: Union[str, Sequence[str], None] = '7611a4f9c6cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", Column("user_id", Integer(), nullable=False),
                  )
    op.create_foreign_key("fk_posts_users", "posts", "users",
                          ["user_id"], ["id"],
                          ondelete="CASCADE"
                          )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_posts_users", "posts")
    op.drop_column("posts", "user_id")
