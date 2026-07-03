from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserInvitationCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole


class UserInvitationResponse(BaseModel):
    message: str
    invitation_token: str | None = None

    model_config = {
        "from_attributes": True,
    }