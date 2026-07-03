from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.equipment_service import list_equipment_for_user
from app.schemas.equipment import EquipmentSummaryResponse


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