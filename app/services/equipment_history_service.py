from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.equipment import Equipment
from app.models.service_job import ServiceJob
from app.models.service_job_item import ServiceJobItem


def get_equipment_history(
    db: Session,
    equipment_id: int,
    company_id: int,
) -> list[dict]:
    equipment = db.scalar(
        select(Equipment).where(
            Equipment.id == equipment_id,
            Equipment.company_id == company_id,
        )
    )

    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found",
        )

    jobs = (
        db.execute(
            select(ServiceJob)
            .join(ServiceJobItem)
            .where(
                ServiceJobItem.equipment_id == equipment_id,
                ServiceJob.company_id == company_id,
            )
            .order_by(ServiceJob.created_at.desc())
        )
        .scalars()
        .all()
    )

    history = []

    for job in jobs:
        history.append(
            {
                "type": "job",
                "id": job.id,
                "reference_number": job.reference_number,
                "status": job.status.value,
                "job_type": job.job_type.value,
                "description": job.description,
                "created_at": job.created_at,
            }
        )

    return history