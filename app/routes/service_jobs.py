from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.service_job import (
    ServiceJobDetailResponse,
    ServiceJobSummaryResponse,
)
from app.services.service_job_service import (
    get_service_job_for_user,
    list_service_jobs_for_user,
)

router = APIRouter(prefix="/service-jobs", tags=["service-jobs"])


@router.get(
    "",
    response_model=list[ServiceJobSummaryResponse],
)
def list_service_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_service_jobs_for_user(
        db=db,
        current_user=current_user,
    )


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

    return job