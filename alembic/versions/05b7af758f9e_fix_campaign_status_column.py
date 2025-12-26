"""fix campaign status column

Revision ID: 05b7af758f9e
Revises: 5046da9694a0
Create Date: 2025-12-26 16:53:31.229235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05b7af758f9e'
down_revision: Union[str, Sequence[str], None] = '5046da9694a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('campaigns', 'status',
               type_=sa.VARCHAR(length=6),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('campaigns', 'status',
               type_=sa.VARCHAR(length=6), # There is no way to know the previous type
               nullable=False)