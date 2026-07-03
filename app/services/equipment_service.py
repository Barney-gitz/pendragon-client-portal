from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.user import User
from app.schemas.equipment import EquipmentSummaryResponse


def list_equipment_for_user(
    db: Session,
    current_user: User,
) -> list[EquipmentSummaryResponse]:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.company_id == current_user.company_id)
        .order_by(Equipment.make, Equipment.model)
        .all()
    )

    return [
        EquipmentSummaryResponse(
            id=machine.id,
            make=machine.make,
            model=machine.model,
            serial_number=machine.serial_number,
            company=machine.company.name,
            primary_contact=(
                f"{machine.primary_contact.first_name} "
                f"{machine.primary_contact.last_name}"
            ),
            is_active=machine.is_active,
        )
        for machine in equipment
    ]