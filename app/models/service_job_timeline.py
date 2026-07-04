from sqlalchemy import Enum as SqlEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.service_job import JobStatus


class ServiceJobTimeline(BaseModel):
    __tablename__ = "service_job_timeline"

    service_job_id: Mapped[int] = mapped_column(
        ForeignKey("service_jobs.id"),
        nullable=False,
    )

    status: Mapped[JobStatus] = mapped_column(
        SqlEnum(JobStatus, name="job_status"),
        nullable=False,
    )

    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    service_job = relationship(
        "ServiceJob",
        back_populates="timeline_entries",
    )

    created_by_user = relationship("User")