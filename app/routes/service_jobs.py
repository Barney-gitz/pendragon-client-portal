from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.service_job import ServiceJobDetailResponse
from app.services.service_job_service import (
    get_service_job_for_user,
    list_service_jobs_for_user,
)

router = APIRouter(prefix="/service-jobs", tags=["service-jobs"])


@router.get("")
def list_service_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = list_service_jobs_for_user(
        db=db,
        current_user=current_user,
    )

    return [
        {
            "id": job.id,
            "reference_number": job.reference_number,
            "company": job.company.name,
            "job_type": job.job_type,
            "status": job.status,
            "description": job.description,
            "is_active": job.is_active,
        }
        for job in jobs
    ]

@router.get(
    "/{job_id}",
    response_model=ServiceJobDetailResponse,
)
def get_service_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_service_job_for_user(
        db=db,
        job_id=job_id,
        current_user=current_user,
    )

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return ServiceJobDetailResponse(
        id=job.id,
        reference_number=job.reference_number,
        company=job.company.name,
        job_type=job.job_type.value,
        status=job.status.value,
        description=job.description,
        items=[
            {
                "make": item.equipment.make,
                "model": item.equipment.model,
                "serial_number": item.equipment.serial_number,
                "contact_name": (
                    f"{item.contact_user.first_name} "
                    f"{item.contact_user.last_name}"
                ),
                "assigned_engineer": (
                    None
                    if item.assigned_engineer is None
                    else (
                        f"{item.assigned_engineer.first_name} "
                        f"{item.assigned_engineer.last_name}"
                    )
                ),
                "sir_number": item.sir_number,
                "started_at": item.started_at,
                "completed_at": item.completed_at,
            }
            for item in job.items
        ],
    )