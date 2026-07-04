from sqlalchemy.orm import Session

from app.models.service_job import JobStatus, ServiceJob
from app.models.service_job_timeline import ServiceJobTimeline
from app.models.user import User


def create_timeline_entry(
    db: Session,
    *,
    service_job: ServiceJob,
    status: JobStatus,
    user: User,
    notes: str | None = None,
) -> ServiceJobTimeline:
    timeline_entry = ServiceJobTimeline(
        service_job_id=service_job.id,
        status=status,
        created_by_user_id=user.id,
        notes=notes,
    )

    db.add(timeline_entry)

    return timeline_entry