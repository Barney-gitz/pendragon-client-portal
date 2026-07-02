from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Equipment(BaseModel):
    __tablename__ = "equipment"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    primary_contact_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    make: Mapped[str] = mapped_column(String(255), nullable=False)

    model: Mapped[str] = mapped_column(String(255), nullable=False)

    serial_number: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    company = relationship("Company", back_populates="equipment")

    primary_contact = relationship(
        "User",
        back_populates="primary_equipment",
        foreign_keys=[primary_contact_user_id],
    )

    service_job_items = relationship("ServiceJobItem", back_populates="equipment")