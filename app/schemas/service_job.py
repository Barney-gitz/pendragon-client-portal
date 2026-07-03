from datetime import datetime

from pydantic import BaseModel


class ServiceJobItemResponse(BaseModel):
    make: str
    model: str
    serial_number: str

    contact_name: str

    assigned_engineer: str | None

    sir_number: str | None

    started_at: datetime | None
    completed_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


class ServiceJobDetailResponse(BaseModel):
    id: int

    reference_number: str

    company: str

    job_type: str

    status: str

    description: str

    items: list[ServiceJobItemResponse]

    model_config = {
        "from_attributes": True,
    }