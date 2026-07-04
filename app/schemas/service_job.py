from datetime import datetime

from app.models.service_job import JobType

from pydantic import BaseModel, ConfigDict


class ServiceJobItemResponse(BaseModel):
    make: str
    model: str
    serial_number: str

    contact_name: str

    assigned_engineer: str | None

    sir_number: str | None

    started_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ServiceJobSummaryResponse(BaseModel):
    id: int

    reference_number: str

    company: str

    job_type: str

    status: str

    description: str

    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ServiceJobDetailResponse(BaseModel):
    id: int

    reference_number: str

    company: str

    job_type: str

    status: str

    description: str

    items: list[ServiceJobItemResponse]

    model_config = ConfigDict(from_attributes=True)


class ServiceJobCreate(BaseModel):
    company_id: int
    reference_number: str
    job_type: JobType
    description: str