from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.equipment import (
    EquipmentCurrentJobResponse,
    EquipmentDetailResponse,
    EquipmentHistoryItemResponse,
    EquipmentSummaryResponse,
)
from app.services.equipment_service import (
    get_current_equipment_job_for_user,
    get_equipment_for_user,
    get_equipment_history_for_user,
    list_equipment_for_user,
)


router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get(
    "",
    response_model=list[EquipmentSummaryResponse],
)
def list_equipment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_equipment_for_user(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{equipment_id}/current-job",
    response_model=EquipmentCurrentJobResponse | None,
)
def get_current_equipment_job(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_current_equipment_job_for_user(
        db=db,
        equipment_id=equipment_id,
        current_user=current_user,
    )


@router.get(
    "/{equipment_id}/history",
    response_model=list[EquipmentHistoryItemResponse],
)
def get_equipment_history(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = get_equipment_history_for_user(
        db=db,
        equipment_id=equipment_id,
        current_user=current_user,
    )

    if history is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return history


@router.get(
    "/{equipment_id}",
    response_model=EquipmentDetailResponse,
)
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    equipment = get_equipment_for_user(
        db=db,
        equipment_id=equipment_id,
        current_user=current_user,
    )

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment