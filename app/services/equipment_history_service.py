from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.service_job_item import ServiceJobItem
from app.models.user import User
from app.schemas.equipment import EquipmentHistoryItemResponse
from app.models.history_event import EquipmentHistoryEvent


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

    events: list[EquipmentHistoryEvent] = []

    for item in items:
        events.append(
            EquipmentHistoryEvent(
                type="machine_logged",
                title="Machine logged for service",
                occurred_at=item.created_at,
                actor=None,
                payload={
                    "service_job_id": item.service_job.id,
                    "service_job_item_id": item.id,
                    "reference_number": item.service_job.reference_number,
                    "job_type": item.service_job.job_type.value,
                    "status": item.service_job.status.value,
                    "description": item.service_job.description,
                    "assigned_engineer": (
                        None
                        if item.assigned_engineer is None
                        else (
                            f"{item.assigned_engineer.first_name} "
                            f"{item.assigned_engineer.last_name}"
                        )
                    ),
                    "started_at": item.started_at,
                    "completed_at": item.completed_at,
                    "created_at": item.created_at,
                },
            )
        )

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