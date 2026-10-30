"""create posts table

Revision ID: 460d500132b8
Revises: 
Create Date: 2026-10-28 20:18:19.093748

"""
from typing import Sequence, Union
from sqlalchemy import Integer, VARCHAR, NVARCHAR, Column, String

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '460d500132b8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
                    Column('id', Integer(), autoincrement=True,
                           primary_key=True, nullable=False),
                    Column('title', VARCHAR(60), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

    pass
