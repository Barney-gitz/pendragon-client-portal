from fastapi import status

from app.models.service_job import JobStatus, JobType, ServiceJob
from app.models.service_job_item import ServiceJobItem


def test_can_view_equipment_history(
    admin_client,
    db,
    company,
    admin_user,
    equipment,
):

    service_job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-3000",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.COMPLETED,
        description="History test",
        is_active=True,
    )

    db.add(service_job)
    db.flush()

    item = ServiceJobItem(
        service_job_id=service_job.id,
        equipment_id=equipment.id,
        contact_user_id=admin_user.id,
    )

    db.add(item)
    db.commit()

    response = admin_client.get(
        f"/equipment/{equipment.id}/history"
    )

    assert response.status_code == status.HTTP_200_OK

    history = response.json()

    assert len(history) == 1

    assert history[0]["reference_number"] == "SJ-3000"
    assert history[0]["status"] == "completed"
    assert history[0]["type"] == "machine_logged"
    assert history[0]["title"] == "Machine logged for service"
    assert history[0]["description"] == "History test"
    assert history[0]["occurred_at"] is not None


def test_unknown_equipment_returns_404(
    admin_client,
):
    response = admin_client.get(
        "/equipment/999999/history"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND