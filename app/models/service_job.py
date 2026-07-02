from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class JobType(str, Enum):
    ONSITE_SERVICE = "onsite_service"
    ONSITE_REPAIR = "onsite_repair"
    ONSITE_CALIBRATION = "onsite_calibration"
    WORKSHOP_REPAIR = "workshop_repair"


class JobStatus(str, Enum):
    RECEIVED = "received"
    AWAITING_INSPECTION = "awaiting_inspection"
    READY_FOR_QUOTE = "ready_for_quote"
    AWAITING_CUSTOMER_APPROVAL = "awaiting_customer_approval"
    WAITING_FOR_PARTS = "waiting_for_parts"
    RETURN_TO_FIT = "return_to_fit"
    IN_REPAIR = "in_repair"
    READY_FOR_RETURN = "ready_for_return"
    COMPLETED = "completed"
    CLOSED = "closed"


class ServiceJob(BaseModel):
    __tablename__ = "service_jobs"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    reference_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    job_type: Mapped[JobType] = mapped_column(
        SqlEnum(JobType, name="job_type"),
        nullable=False,
    )

    status: Mapped[JobStatus] = mapped_column(
        SqlEnum(JobStatus, name="job_status"),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)