"""add status to service job items

Revision ID: f5d4a0cc0337
Revises: aa6b61474d11
Create Date: 2026-07-05 19:47:52.820337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f5d4a0cc0337'
down_revision: Union[str, Sequence[str], None] = 'aa6b61474d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    service_job_item_status = postgresql.ENUM(
        "PENDING",
        "ASSIGNED",
        "IN_PROGRESS",
        "AWAITING_PARTS",
        "TESTING",
        "READY_FOR_RETURN",
        "COMPLETED",
        "CANCELLED",
        name="service_job_item_status",
    )
    service_job_item_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "service_job_items",
        sa.Column(
            "status",
            service_job_item_status,
            server_default="PENDING",
            nullable=False,
        ),
    )

    op.alter_column(
        "service_job_items",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("service_job_items", "status")

    service_job_item_status = postgresql.ENUM(
        "PENDING",
        "ASSIGNED",
        "IN_PROGRESS",
        "AWAITING_PARTS",
        "TESTING",
        "READY_FOR_RETURN",
        "COMPLETED",
        "CANCELLED",
        name="service_job_item_status",
    )
    service_job_item_status.drop(op.get_bind(), checkfirst=True)