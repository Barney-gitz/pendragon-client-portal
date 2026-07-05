from fastapi import status

from app.models.service_job import JobStatus, JobType, ServiceJob
from app.models.service_job_item import ServiceJobItem, ServiceJobItemStatus
from app.models.service_job_item_timeline import ServiceJobItemTimeline


def test_updating_job_item_status_creates_timeline_entry(
    admin_client,
    db,
    company,
    admin_user,
    equipment,
):
    job = ServiceJob(
        company_id=company.id,
        reference_number="SJ-6000",
        job_type=JobType.ONSITE_SERVICE,
        status=JobStatus.RECEIVED,
        description="Item timeline test.",
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
    db.refresh(item)

    response = admin_client.patch(
        f"/service-job-items/{item.id}",
        json={
            "status": "awaiting_parts",
            "notes": "Waiting on replacement PCB.",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    db.refresh(item)
    assert item.status == ServiceJobItemStatus.AWAITING_PARTS

    timeline_entries = (
        db.query(ServiceJobItemTimeline)
        .filter(ServiceJobItemTimeline.service_job_item_id == item.id)
        .all()
    )

    assert len(timeline_entries) == 1
    assert timeline_entries[0].status == ServiceJobItemStatus.AWAITING_PARTS