from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.service_job_item import ServiceJobItem
from app.models.user import User
from app.schemas.equipment import EquipmentHistoryItemResponse
from app.services.history.machine_logged_events import build_machine_logged_events


def get_equipment_history_for_user(
    db: Session,
    equipment_id: int,
    current_user: User,
) -> list[EquipmentHistoryItemResponse] | None:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .filter(Equipment.company_id == current_user.company_id)
        .first()
    )

    if equipment is None:
        return None

    items = (
        db.query(ServiceJobItem)
        .filter(ServiceJobItem.equipment_id == equipment.id)
        .join(ServiceJobItem.service_job)
        .order_by(ServiceJobItem.created_at.desc())
        .all()
    )

    events = build_machine_logged_events(items)

    events.sort(key=lambda event: event.occurred_at, reverse=True)

    return [
        EquipmentHistoryItemResponse(
            type=event.type,
            title=event.title,
            occurred_at=event.occurred_at,
            **event.payload,
        )
        for event in events
    ]