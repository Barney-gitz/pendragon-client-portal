from sqlalchemy.orm import Session

from app.models.service_job_item import ServiceJobItem
from app.models.service_job_item import ServiceJobItemStatus
from app.models.service_job import ServiceJob
from app.services.service_job_item_timeline_service import (
    create_timeline_entry,
)
from app.models.user import User


def update_job_item_status(
    db: Session,
    *,
    job_item: ServiceJobItem,
    status: ServiceJobItemStatus,
    user: User,
) -> ServiceJobItem:
    if job_item.status == status:
        return job_item

    job_item.status = status

    create_timeline_entry(
        db=db,
        job_item=job_item,
        user=user,
        status=status,
    )

    db.flush()

    return job_item


def update_service_job_item_for_user(
    db: Session,
    *,
    item_id: int,
    status: ServiceJobItemStatus,
    notes: str | None,
    current_user: User,
) -> ServiceJobItem | None:
    item = (
        db.query(ServiceJobItem)
        .join(ServiceJob)
        .filter(ServiceJobItem.id == item_id)
        .filter(ServiceJob.company_id == current_user.company_id)
        .first()
    )

    if item is None:
        return None

    return update_job_item_status(
        db=db,
        job_item=item,
        status=status,
        user=current_user,
    )