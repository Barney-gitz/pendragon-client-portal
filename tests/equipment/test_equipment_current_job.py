from fastapi import status

from app.models.service_job import JobStatus, JobType, ServiceJob
from app.models.service_job_item import ServiceJobItem


def test_returns_current_equipment_job(
    admin_client,
    db,
    company,
    admin_user,
    equipment,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-4000",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Current job",
        is_active=True,
    )

    db.add(job)
    db.flush()

    item = ServiceJobItem(
        service_job_id=job.id,
        equipment_id=equipment.id,
        contact_user_id=admin_user.id,
    )

    db.add(item)
    db.commit()

    response = admin_client.get(
        f"/equipment/{equipment.id}/current-job"
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["reference_number"] == "SJ-4000"
    assert data["status"] == "received"


def test_returns_null_when_no_current_job(
    admin_client,
    equipment,
):
    response = admin_client.get(
        f"/equipment/{equipment.id}/current-job"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


def test_completed_jobs_are_not_current(
    admin_client,
    db,
    company,
    admin_user,
    equipment,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-5000",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.COMPLETED,
        description="Completed job",
        is_active=True,
    )

    db.add(job)
    db.flush()

    item = ServiceJobItem(
        service_job_id=job.id,
        equipment_id=equipment.id,
        contact_user_id=admin_user.id,
    )

    db.add(item)
    db.commit()

    response = admin_client.get(
        f"/equipment/{equipment.id}/current-job"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None