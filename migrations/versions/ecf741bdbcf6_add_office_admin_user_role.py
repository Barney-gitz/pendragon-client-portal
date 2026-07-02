"""add office admin user role

Revision ID: ecf741bdbcf6
Revises: 63655ad49f6a
Create Date: 2026-07-02 16:22:51.547302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecf741bdbcf6'
down_revision: Union[str, Sequence[str], None] = '63655ad49f6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'PENDRAGON_OFFICE_ADMIN'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL does not support removing enum values.
    # A downgrade would require recreating the enum type,
    # which isn't worth the complexity for development.
    pass
