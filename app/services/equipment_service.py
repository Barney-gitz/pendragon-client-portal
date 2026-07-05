from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.user import User
from app.models.service_job_item import ServiceJobItem
from app.models.service_job import JobStatus, ServiceJob
from app.schemas.equipment import (
    EquipmentCurrentJobResponse,
    EquipmentDetailResponse,
    EquipmentHistoryItemResponse,
    EquipmentSummaryResponse,
)


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


def get_equipment_for_user(
    db: Session,
    equipment_id: int,
    current_user: User,
) -> EquipmentDetailResponse | None:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .filter(Equipment.company_id == current_user.company_id)
        .first()
    )

    if equipment is None:
        return None

    return EquipmentDetailResponse(
        id=equipment.id,
        make=equipment.make,
        model=equipment.model,
        serial_number=equipment.serial_number,
        company=equipment.company.name,
        primary_contact=(
            f"{equipment.primary_contact.first_name} "
            f"{equipment.primary_contact.last_name}"
        ),
        is_active=equipment.is_active,
    )


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

    return [
        EquipmentHistoryItemResponse(
            service_job_id=item.service_job.id,
            service_job_item_id=item.id,
            reference_number=item.service_job.reference_number,
            job_type=item.service_job.job_type.value,
            status=item.service_job.status.value,
            description=item.service_job.description,
            assigned_engineer=(
                None
                if item.assigned_engineer is None
                else (
                    f"{item.assigned_engineer.first_name} "
                    f"{item.assigned_engineer.last_name}"
                )
            ),
            started_at=item.started_at,
            completed_at=item.completed_at,
            created_at=item.created_at,
        )
        for item in items
    ]


def get_current_equipment_job_for_user(
    db: Session,
    equipment_id: int,
    current_user: User,
) -> EquipmentCurrentJobResponse | None:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .filter(Equipment.company_id == current_user.company_id)
        .first()
    )

    if equipment is None:
        return None

    item = (
        db.query(ServiceJobItem)
        .filter(ServiceJobItem.equipment_id == equipment.id)
        .join(ServiceJobItem.service_job)
        .filter(ServiceJobItem.service_job.has(ServiceJob.status.notin_([
            JobStatus.COMPLETED,
            JobStatus.CLOSED,
        ])))
        .order_by(ServiceJobItem.created_at.desc())
        .first()
    )

    if item is None:
        return None

    return EquipmentCurrentJobResponse(
        service_job_id=item.service_job.id,
        service_job_item_id=item.id,
        reference_number=item.service_job.reference_number,
        job_type=item.service_job.job_type.value,
        status=item.service_job.status.value,
        description=item.service_job.description,
        assigned_engineer=(
            None
            if item.assigned_engineer is None
            else (
                f"{item.assigned_engineer.first_name} "
                f"{item.assigned_engineer.last_name}"
            )
        ),
        started_at=item.started_at,
        created_at=item.created_at,
    )