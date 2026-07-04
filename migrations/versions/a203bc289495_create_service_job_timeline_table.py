"""create service job timeline table

Revision ID: a203bc289495
Revises: deacf5048459
Create Date: 2026-07-03 23:32:26.880640

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a203bc289495'
down_revision: Union[str, Sequence[str], None] = 'deacf5048459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "service_job_timeline",
        sa.Column("service_job_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "RECEIVED",
                "AWAITING_INSPECTION",
                "READY_FOR_QUOTE",
                "AWAITING_CUSTOMER_APPROVAL",
                "WAITING_FOR_PARTS",
                "RETURN_TO_FIT",
                "IN_REPAIR",
                "READY_FOR_RETURN",
                "COMPLETED",
                "CLOSED",
                name="job_status",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name=op.f("fk_service_job_timeline_created_by_user_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["service_job_id"],
            ["service_jobs.id"],
            name=op.f("fk_service_job_timeline_service_job_id_service_jobs"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_service_job_timeline")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("service_job_timeline")