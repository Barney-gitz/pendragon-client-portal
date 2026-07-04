from enum import Enum
from typing import Any

from sqlalchemy import Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class AuditCategory(str, Enum):
    BUSINESS = "business"
    ADMIN = "admin"
    SECURITY = "security"


class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PASSWORD_RESET_REQUESTED = "password_reset_requested"
    PASSWORD_RESET_COMPLETED = "password_reset_completed"
    LOGIN_FAILED = "login_failed"
    SUSPICIOUS_LOGIN = "suspicious_login"


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    category: Mapped[AuditCategory] = mapped_column(
        SqlEnum(AuditCategory, name="audit_category"),
        nullable=False,
    )

    action: Mapped[AuditAction] = mapped_column(
        SqlEnum(AuditAction, name="audit_action"),
        nullable=False,
    )

    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    old_values: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_values: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    event_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    actor_user = relationship(
        "User",
        foreign_keys=[actor_user_id],
    )