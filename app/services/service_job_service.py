from sqlalchemy.orm import Session

from app.models.service_job import ServiceJob
from app.models.user import User, UserRole
from app.models.service_job_item import ServiceJobItem
from app.schemas.service_job import (
    ServiceJobItemResponse,
    ServiceJobSummaryResponse,
    ServiceJobDetailResponse,
)


def list_service_jobs_for_user(
    db: Session,
    current_user: User,
) -> list[ServiceJobSummaryResponse]:
    query = db.query(ServiceJob)

    if current_user.role == UserRole.PENDRAGON_ADMIN:
        pass

    elif current_user.role == UserRole.PENDRAGON_ENGINEER:
        query = (
            query
            .join(ServiceJobItem)
            .filter(ServiceJobItem.assigned_engineer_id == current_user.id)
        )

    else:
        query = query.filter(
            ServiceJob.company_id == current_user.company_id
        )

    jobs = (
        query
        .distinct()
        .order_by(ServiceJob.reference_number)
        .all()
    )

    return [
        ServiceJobSummaryResponse(
            id=job.id,
            reference_number=job.reference_number,
            company=job.company.name,
            job_type=job.job_type.value,
            status=job.status.value,
            description=job.description,
            is_active=job.is_active,
        )
        for job in jobs
    ]


def get_service_job_for_user(
    db: Session,
    job_id: int,
    current_user: User,
) -> ServiceJobDetailResponse | None:
    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.id == job_id)
        .filter(ServiceJob.company_id == current_user.company_id)
        .first()
    )

    if job is None:
        return None

    return ServiceJobDetailResponse(
        id=job.id,
        reference_number=job.reference_number,
        company=job.company.name,
        job_type=job.job_type.value,
        status=job.status.value,
        description=job.description,
        items=[
            ServiceJobItemResponse(
                make=item.equipment.make,
                model=item.equipment.model,
                serial_number=item.equipment.serial_number,
                contact_name=(
                    f"{item.contact_user.first_name} "
                    f"{item.contact_user.last_name}"
                ),
                assigned_engineer=(
                    None
                    if item.assigned_engineer is None
                    else (
                        f"{item.assigned_engineer.first_name} "
                        f"{item.assigned_engineer.last_name}"
                    )
                ),
                sir_number=item.sir_number,
                started_at=item.started_at,
                completed_at=item.completed_at,
            )
            for item in job.items
        ],
    )