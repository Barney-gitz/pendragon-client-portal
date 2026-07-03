from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.equipment import Equipment

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("")
def list_equipment(db: Session = Depends(get_db)):
    equipment = (
        db.query(Equipment)
        .order_by(Equipment.make, Equipment.model)
        .all()
    )

    return [
        {
            "id": machine.id,
            "make": machine.make,
            "model": machine.model,
            "serial_number": machine.serial_number,
            "company": machine.company.name,
            "primary_contact": (
                f"{machine.primary_contact.first_name} "
                f"{machine.primary_contact.last_name}"
            ),
            "is_active": machine.is_active,
        }
        for machine in equipment
    ]