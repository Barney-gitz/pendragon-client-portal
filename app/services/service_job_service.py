from sqlalchemy.orm import Session

from app.models.service_job import ServiceJob
from app.models.user import User


def list_service_jobs_for_user(
    db: Session,
    current_user: User,
) -> list[ServiceJob]:
    return (
        db.query(ServiceJob)
        .filter(ServiceJob.company_id == current_user.company_id)
        .order_by(ServiceJob.reference_number)
        .all()
    )


def get_service_job_for_user(
    db: Session,
    job_id: int,
    current_user: User,
) -> ServiceJob | None:
    return (
        db.query(ServiceJob)
        .filter(ServiceJob.id == job_id)
        .filter(ServiceJob.company_id == current_user.company_id)
        .first()
    )