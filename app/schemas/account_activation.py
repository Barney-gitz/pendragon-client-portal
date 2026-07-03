from pydantic import BaseModel, Field


class AccountActivationRequest(BaseModel):
    token: str

    password: str = Field(
        min_length=12,
        max_length=128,
    )

    confirm_password: str = Field(
        min_length=12,
        max_length=128,
    )

class AccountActivationResponse(BaseModel):
    message: str