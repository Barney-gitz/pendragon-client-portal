from enum import Enum
from datetime import datetime

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class UserRole(str, Enum):
    PENDRAGON_ADMIN = "pendragon_admin"
    PENDRAGON_MANAGER = "pendragon_manager"
    PENDRAGON_ENGINEER = "pendragon_engineer"
    PENDRAGON_OFFICE_ADMIN = "pendragon_office_admin"
    CUSTOMER_USER = "customer_user"


class User(BaseModel):
    __tablename__ = "users"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    activated_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    sir_initials: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, name="user_role"),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    company = relationship("Company", back_populates="users")

    primary_equipment = relationship(
        "Equipment",
        back_populates="primary_contact",
        foreign_keys="Equipment.primary_contact_user_id",
    )

    contact_job_items = relationship(
        "ServiceJobItem",
        back_populates="contact_user",
        foreign_keys="ServiceJobItem.contact_user_id",
    )

    assigned_job_items = relationship(
        "ServiceJobItem",
        back_populates="assigned_engineer",
        foreign_keys="ServiceJobItem.assigned_engineer_id",
    )

    service_job_timeline_entries = relationship(
        "ServiceJobTimeline",
        back_populates="created_by_user",
    )

    service_job_item_timeline_entries = relationship(
        "ServiceJobItemTimeline",
        back_populates="created_by_user",
    )