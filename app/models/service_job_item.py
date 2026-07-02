from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ServiceJobItem(BaseModel):
    __tablename__ = "service_job_items"

    service_job_id: Mapped[int] = mapped_column(
        ForeignKey("service_jobs.id"),
        nullable=False,
    )

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        nullable=False,
    )

    contact_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    assigned_engineer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    sir_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(nullable=True)

    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    service_job = relationship("ServiceJob", back_populates="items")
    equipment = relationship("Equipment", back_populates="service_job_items")

    contact_user = relationship(
        "User",
        back_populates="contact_job_items",
        foreign_keys=[contact_user_id],
    )

    assigned_engineer = relationship(
        "User",
        back_populates="assigned_job_items",
        foreign_keys=[assigned_engineer_id],
    )