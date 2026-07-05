from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EquipmentSummaryResponse(BaseModel):
    id: int
    make: str
    model: str
    serial_number: str
    company: str
    primary_contact: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class EquipmentDetailResponse(BaseModel):
    id: int
    make: str
    model: str
    serial_number: str
    company: str
    primary_contact: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class EquipmentHistoryItemResponse(BaseModel):
    type: str
    title: str
    occurred_at: datetime

    service_job_id: int
    service_job_item_id: int
    reference_number: str
    job_type: str
    status: str
    description: str
    assigned_engineer: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EquipmentCurrentJobResponse(BaseModel):
    service_job_id: int
    service_job_item_id: int
    reference_number: str
    job_type: str
    status: str
    description: str
    assigned_engineer: str | None
    started_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)