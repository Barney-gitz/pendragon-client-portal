from sqlalchemy.orm import Session

from app.models.service_job_item import ServiceJobItem
from app.models.service_job_item_timeline import (
    ServiceJobItemTimeline,
)
from app.models.user import User


def create_timeline_entry(
    db: Session,
    *,
    job_item: ServiceJobItem,
    user: User,
    status,
    notes: str | None = None,
) -> None:
    entry = ServiceJobItemTimeline(
        service_job_item=job_item,
        created_by_user=user,
        status=status,
        notes=notes,
    )

    db.add(entry)