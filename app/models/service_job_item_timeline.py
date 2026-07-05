from app.models.base import BaseModel
from app.models.service_job_item import ServiceJobItemStatus

from sqlalchemy import Enum as SqlEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ServiceJobItemTimeline(BaseModel):
    __tablename__ = "service_job_item_timeline"

    service_job_item_id: Mapped[int] = mapped_column(
        ForeignKey("service_job_items.id"),
        nullable=False,
    )

    status: Mapped[ServiceJobItemStatus] = mapped_column(
        SqlEnum(
            ServiceJobItemStatus,
            name="service_job_item_status",
            create_type=False,
        ),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    service_job_item = relationship(
        "ServiceJobItem",
        back_populates="timeline_entries",
    )

    created_by_user = relationship(
        "User",
        back_populates="service_job_item_timeline_entries",
    )