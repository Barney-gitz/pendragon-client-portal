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