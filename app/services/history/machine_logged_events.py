from app.models.history_event import EquipmentHistoryEvent
from app.models.service_job_item import ServiceJobItem


def build_machine_logged_events(
    items: list[ServiceJobItem],
) -> list[EquipmentHistoryEvent]:
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

    return events