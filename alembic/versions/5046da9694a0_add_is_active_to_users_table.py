"""add is_active to users table

Revision ID: 5046da9694a0
Revises: 6d7554d01c6d
Create Date: 2025-12-26 16:24:45.050099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5046da9694a0'
down_revision: Union[str, Sequence[str], None] = '6d7554d01c6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_active')
