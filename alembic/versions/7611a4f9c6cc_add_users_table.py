"""add users table

Revision ID: 7611a4f9c6cc
Revises: f71aa1bbd2d8
Create Date: 2026-10-28 20:48:43.030233

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Integer, VARCHAR, NVARCHAR, Column, String, TIMESTAMP, Identity
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '7611a4f9c6cc'
down_revision: Union[str, Sequence[str], None] = 'f71aa1bbd2d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    Column('id', Integer(), Identity(),
                           autoincrement=True, nullable=False),
                    Column('email', String(), nullable=False),
                    Column('password', String(), nullable=False),
                    Column("created_at", TIMESTAMP(timezone=True),
                           server_default=func.current_timestamp(), nullable=False)
                    )

    op.create_primary_key("pk_users", "users", ["id"])
    op.create_unique_constraint("uq_email", "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
