"""rename manufacturer to make and enforce unique serial numbers

Revision ID: 13fa3965ce8b
Revises: ecf741bdbcf6
Create Date: 2026-07-02 22:22:15.729705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13fa3965ce8b'
down_revision: Union[str, Sequence[str], None] = 'ecf741bdbcf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        op.f("uq_equipment_serial_number"),
        "equipment",
        ["serial_number"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("uq_equipment_serial_number"),
        "equipment",
        type_="unique",
    )
