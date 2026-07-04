from fastapi import status

from app.models.service_job import JobStatus, ServiceJob
from app.models.service_job_timeline import ServiceJobTimeline


def test_admin_can_create_service_job(admin_client, db, company):
    payload = {
        "company_id": company.id,
        "reference_number": "SJ-1000",
        "job_type": "onsite_service",
        "description": "Customer reports intermittent fault.",
    }

    response = admin_client.post(
        "/service-jobs",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.reference_number == "SJ-1000")
        .first()
    )

    assert job is not None
    assert job.status == JobStatus.RECEIVED


def test_creating_service_job_creates_timeline_entry(
    admin_client,
    db,
    company,
):
    payload = {
        "company_id": company.id,
        "reference_number": "SJ-1001",
        "job_type": "onsite_service",
        "description": "Timeline creation test.",
    }

    response = admin_client.post(
        "/service-jobs",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    job = (
        db.query(ServiceJob)
        .filter(ServiceJob.reference_number == "SJ-1001")
        .first()
    )

    timeline = (
        db.query(ServiceJobTimeline)
        .filter(ServiceJobTimeline.service_job_id == job.id)
        .all()
    )

    assert len(timeline) == 1
    assert timeline[0].status == JobStatus.RECEIVED
    assert timeline[0].notes == "Service job created."


def test_engineer_cannot_create_service_job(
    engineer_client,
    company,
):
    payload = {
        "company_id": company.id,
        "reference_number": "SJ-1002",
        "job_type": "onsite_service",
        "description": "Permission test.",
    }

    response = engineer_client.post(
        "/service-jobs",
        json=payload,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN