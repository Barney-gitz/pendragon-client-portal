from pydantic import BaseModel


class DashboardUserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    company: str


class DashboardResponse(BaseModel):
    current_user: DashboardUserResponse
    equipment_count: int
    open_jobs: int
    completed_jobs: int
    awaiting_quote: int