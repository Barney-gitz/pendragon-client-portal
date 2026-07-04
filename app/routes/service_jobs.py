from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.service_job_timeline import ServiceJobTimelineResponse
from fastapi import status

from app.auth.permissions import require_roles
from app.models.user import UserRole
from app.schemas.service_job import ServiceJobCreate
from app.schemas.service_job import (
    ServiceJobDetailResponse,
    ServiceJobSummaryResponse,
)
from app.services.service_job_service import (
    create_service_job,
    get_service_job_for_user,
    list_service_jobs_for_user,
    list_service_job_timeline_for_user,
)
from app.services.service_job_service import (
    get_service_job_for_user,
    list_service_jobs_for_user,
    list_service_job_timeline_for_user,
)

router = APIRouter(prefix="/service-jobs", tags=["service-jobs"])


@router.post(
    "",
    response_model=ServiceJobSummaryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    payload: ServiceJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.PENDRAGON_ADMIN,
            UserRole.PENDRAGON_MANAGER,
            UserRole.PENDRAGON_OFFICE_ADMIN,
        )
    ),
):
    try:
        job = create_service_job(
            db=db,
            company_id=payload.company_id,
            reference_number=payload.reference_number,
            job_type=payload.job_type,
            description=payload.description,
            current_user=current_user,
        )

    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return ServiceJobSummaryResponse(
        id=job.id,
        reference_number=job.reference_number,
        company=job.company.name,
        job_type=job.job_type.value,
        status=job.status.value,
        description=job.description,
        is_active=job.is_active,
    )


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
    "/{job_id}/timeline",
    response_model=list[ServiceJobTimelineResponse],
)
def list_service_job_timeline(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    timeline = list_service_job_timeline_for_user(
        db=db,
        job_id=job_id,
        current_user=current_user,
    )

    if timeline is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return timeline


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