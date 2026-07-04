from typing import Any

from sqlalchemy.orm import Session
from app.models.service_job import JobStatus, ServiceJob

from app.models.audit_log import (
    AuditAction,
    AuditCategory,
    AuditLog,
)
from app.models.user import User


def record_audit_event(
    db: Session,
    *,
    category: AuditCategory,
    action: AuditAction,
    actor: User | None,
    entity_type: str,
    entity_id: int | None = None,
    old_values: dict[str, Any] | None = None,
    new_values: dict[str, Any] | None = None,
    event_metadata: dict[str, Any] | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> AuditLog:
    """
    Record an audit event.

    This function intentionally does not commit the transaction.
    The caller is responsible for committing so the audit event
    becomes part of the same database transaction.
    """

    audit = AuditLog(
        category=category,
        action=action,
        actor_user_id=None if actor is None else actor.id,
        entity_type=entity_type,
        entity_id=entity_id,
        old_values=old_values,
        new_values=new_values,
        event_metadata=event_metadata,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(audit)

    return audit


def record_service_job_created(
    db: Session,
    *,
    service_job: ServiceJob,
    actor: User,
) -> AuditLog:
    return record_audit_event(
        db=db,
        category=AuditCategory.BUSINESS,
        action=AuditAction.CREATE,
        actor=actor,
        entity_type="service_job",
        entity_id=service_job.id,
        new_values={
            "reference_number": service_job.reference_number,
            "status": service_job.status.value,
            "job_type": service_job.job_type.value,
            "description": service_job.description,
        },
    )


def record_service_job_updated(
    db: Session,
    *,
    service_job: ServiceJob,
    actor: User,
    old_status: JobStatus,
) -> AuditLog:
    return record_audit_event(
        db=db,
        category=AuditCategory.BUSINESS,
        action=AuditAction.UPDATE,
        actor=actor,
        entity_type="service_job",
        entity_id=service_job.id,
        old_values={
            "status": old_status.value,
        },
        new_values={
            "status": service_job.status.value,
        },
    )


