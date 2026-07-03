from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.service_job import JobStatus, ServiceJob
from app.models.service_job_item import ServiceJobItem
from app.models.user import User, UserRole
from app.schemas.dashboard import DashboardResponse, DashboardUserResponse


INTERNAL_ADMIN_ROLES = {
    UserRole.PENDRAGON_ADMIN,
    UserRole.PENDRAGON_MANAGER,
    UserRole.PENDRAGON_OFFICE_ADMIN,
}


def get_dashboard_summary(
    db: Session,
    current_user: User,
) -> DashboardResponse:
    job_query = db.query(ServiceJob)
    equipment_query = db.query(Equipment)

    if current_user.role in INTERNAL_ADMIN_ROLES:
        pass

    elif current_user.role == UserRole.PENDRAGON_ENGINEER:
        job_query = (
            job_query
            .join(ServiceJobItem)
            .filter(ServiceJobItem.assigned_engineer_id == current_user.id)
        )

        equipment_query = (
            equipment_query
            .join(ServiceJobItem)
            .filter(ServiceJobItem.assigned_engineer_id == current_user.id)
        )

    else:
        job_query = job_query.filter(
            ServiceJob.company_id == current_user.company_id
        )

        equipment_query = equipment_query.filter(
            Equipment.company_id == current_user.company_id
        )

    equipment_count = (
        equipment_query
        .with_entities(func.count(func.distinct(Equipment.id)))
        .scalar()
    )

    open_jobs = (
        job_query
        .filter(ServiceJob.status.notin_([JobStatus.COMPLETED, JobStatus.CLOSED]))
        .with_entities(func.count(func.distinct(ServiceJob.id)))
        .scalar()
    )

    completed_jobs = (
        job_query
        .filter(ServiceJob.status == JobStatus.COMPLETED)
        .with_entities(func.count(func.distinct(ServiceJob.id)))
        .scalar()
    )

    awaiting_quote = (
        job_query
        .filter(ServiceJob.status == JobStatus.READY_FOR_QUOTE)
        .with_entities(func.count(func.distinct(ServiceJob.id)))
        .scalar()
    )

    return DashboardResponse(
        current_user=DashboardUserResponse(
            id=current_user.id,
            email=current_user.email,
            name=f"{current_user.first_name} {current_user.last_name}",
            role=current_user.role.value,
            company=current_user.company.name,
        ),
        equipment_count=equipment_count or 0,
        open_jobs=open_jobs or 0,
        completed_jobs=completed_jobs or 0,
        awaiting_quote=awaiting_quote or 0,
    )