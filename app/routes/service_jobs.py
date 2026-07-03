from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.session import get_db
from app.models.service_job import ServiceJob
from app.schemas.service_job import ServiceJobDetailResponse

router = APIRouter(prefix="/service-jobs", tags=["service-jobs"])


@router.get("")
def list_service_jobs(db: Session = Depends(get_db)):
    jobs = (
        db.query(ServiceJob)
        .order_by(ServiceJob.reference_number)
        .all()
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
):
    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.id == job_id)
        .first()
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