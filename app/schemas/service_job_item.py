from pydantic import BaseModel

from app.models.service_job_item import ServiceJobItemStatus


class ServiceJobItemUpdate(BaseModel):
    status: ServiceJobItemStatus
    notes: str | None = None