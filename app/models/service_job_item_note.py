from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ServiceJobItemNote(BaseModel):
    __tablename__ = "service_job_item_notes"

    service_job_item_id: Mapped[int] = mapped_column(
        ForeignKey("service_job_items.id"),
        nullable=False,
    )

    author_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    note: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_customer_visible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    service_job_item = relationship(
        "ServiceJobItem",
        back_populates="notes",
    )

    author = relationship(
        "User",
        back_populates="service_job_item_notes",
    )