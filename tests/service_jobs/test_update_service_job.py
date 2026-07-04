from fastapi import status

from app.models.service_job import JobStatus, JobType, ServiceJob

from app.models.audit_log import AuditAction, AuditCategory, AuditLog


def test_admin_can_update_service_job_status(
    admin_client,
    db,
    company,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-2000",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Status update test.",
        is_active=True,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    response = admin_client.patch(
        f"/service-jobs/{job.id}",
        json={
            "status": "in_repair",
            "notes": "Engineer has started repair.",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    db.refresh(job)

    assert job.status == JobStatus.IN_REPAIR


from app.models.service_job_timeline import ServiceJobTimeline


def test_updating_service_job_status_creates_timeline_entry(
    admin_client,
    db,
    company,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-2001",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Timeline update test.",
        is_active=True,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    response = admin_client.patch(
        f"/service-jobs/{job.id}",
        json={
            "status": "in_repair",
            "notes": "Engineer has started repair.",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    timeline_entries = (
        db.query(ServiceJobTimeline)
        .filter(ServiceJobTimeline.service_job_id == job.id)
        .all()
    )

    assert len(timeline_entries) == 1
    assert timeline_entries[0].status == JobStatus.IN_REPAIR
    assert timeline_entries[0].notes == "Engineer has started repair."


def test_updating_service_job_status_creates_audit_log(
    admin_client,
    db,
    company,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-2002",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Audit update test.",
        is_active=True,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    response = admin_client.patch(
        f"/service-jobs/{job.id}",
        json={
            "status": "in_repair",
            "notes": "Engineer started repair.",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    audit = (
        db.query(AuditLog)
        .filter(AuditLog.entity_type == "service_job")
        .filter(AuditLog.entity_id == job.id)
        .filter(AuditLog.action == AuditAction.UPDATE)
        .first()
    )

    assert audit is not None
    assert audit.category == AuditCategory.BUSINESS

    assert audit.old_values["status"] == "received"
    assert audit.new_values["status"] == "in_repair"


def test_updating_to_same_status_does_not_create_duplicate_history(
    admin_client,
    db,
    company,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-2003",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Duplicate history test.",
        is_active=True,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    response = admin_client.patch(
        f"/service-jobs/{job.id}",
        json={
            "status": "received",
            "notes": "Should not create history.",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    timeline_entries = (
        db.query(ServiceJobTimeline)
        .filter(ServiceJobTimeline.service_job_id == job.id)
        .all()
    )

    audit_entries = (
        db.query(AuditLog)
        .filter(AuditLog.entity_type == "service_job")
        .filter(AuditLog.entity_id == job.id)
        .filter(AuditLog.action == AuditAction.UPDATE)
        .all()
    )

    assert len(timeline_entries) == 0
    assert len(audit_entries) == 0