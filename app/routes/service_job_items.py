from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.service_job_item import ServiceJobItemUpdate
from app.services.service_job_item_service import update_service_job_item_for_user

router = APIRouter(
    prefix="/service-job-items",
    tags=["service-job-items"],
)


@router.patch("/{item_id}")
def update_item(
    item_id: int,
    payload: ServiceJobItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = update_service_job_item_for_user(
        db=db,
        item_id=item_id,
        status=payload.status,
        notes=payload.notes,
        current_user=current_user,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service job item not found.",
        )

    return {"message": "Service job item updated."}