from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceJobTimelineResponse(BaseModel):
    id: int
    status: str
    notes: str | None
    created_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)