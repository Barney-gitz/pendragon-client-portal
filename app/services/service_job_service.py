from sqlalchemy.orm import Session

from app.models.service_job import JobStatus, JobType, ServiceJob
from app.models.user import User, UserRole
from app.models.service_job_item import ServiceJobItem
from app.models.service_job_timeline import ServiceJobTimeline
from app.schemas.service_job_timeline import ServiceJobTimelineResponse
from app.models.company import Company
from app.services.service_job_timeline_service import create_timeline_entry
from app.models.audit_log import AuditAction, AuditCategory
from app.services.audit_service import record_service_job_updated
from app.services.audit_service import (
    record_audit_event,
    record_service_job_created,
)
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


def list_service_job_timeline_for_user(
    db: Session,
    job_id: int,
    current_user: User,
) -> list[ServiceJobTimelineResponse] | None:
    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.id == job_id)
        .filter(ServiceJob.company_id == current_user.company_id)
        .first()
    )

    if job is None:
        return None

    timeline_entries = (
        db.query(ServiceJobTimeline)
        .filter(ServiceJobTimeline.service_job_id == job.id)
        .order_by(ServiceJobTimeline.created_at)
        .all()
    )

    return [
        ServiceJobTimelineResponse(
            id=entry.id,
            status=entry.status.value,
            notes=entry.notes,
            created_by=(
                f"{entry.created_by_user.first_name} "
                f"{entry.created_by_user.last_name}"
            ),
            created_at=entry.created_at,
        )
        for entry in timeline_entries
    ]


def create_service_job(
    db: Session,
    *,
    company_id: int,
    reference_number: str,
    job_type: JobType,
    description: str,
    current_user: User,
) -> ServiceJob:
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .filter(Company.is_active.is_(True))
        .first()
    )

    if company is None:
        raise ValueError("Company not found.")

    service_job = ServiceJob(
        company_id=company_id,
        reference_number=reference_number,
        job_type=job_type,
        status=JobStatus.RECEIVED,
        description=description,
        is_active=True,
    )

    db.add(service_job)
    db.flush()

    create_timeline_entry(
        db=db,
        service_job=service_job,
        status=JobStatus.RECEIVED,
        user=current_user,
        notes="Service job created.",
    )

    record_service_job_created(
        db=db,
        service_job=service_job,
        actor=current_user,
    )

    db.commit()
    db.refresh(service_job)

    return service_job


def update_service_job(
    db: Session,
    *,
    job_id: int,
    status: JobStatus,
    notes: str | None,
    current_user: User,
) -> ServiceJob | None:
    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.id == job_id)
        .filter(ServiceJob.company_id == current_user.company_id)
        .first()
    )

    if job is None:
        return None

    old_status = job.status

    if old_status != status:
        job.status = status

        create_timeline_entry(
            db=db,
            service_job=job,
            status=status,
            user=current_user,
            notes=notes,
        )

        record_service_job_updated(
            db=db,
            service_job=job,
            actor=current_user,
            old_status=old_status,
        )

    db.commit()
    db.refresh(job)

    return job