from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExistsError
from app.core.config import settings
from app.db.session import get_db
from app.schemas.invitation import (
    UserInvitationCreate,
    UserInvitationResponse,
)
from app.services.invitation_service import create_user_invitation
from app.models.user_invitation import UserInvitation
from app.auth.permissions import require_roles
from app.models.user import User, UserRole


router = APIRouter(
    prefix="/companies",
    tags=["invitations"],
)

@router.post(
    "/{company_id}/invitations",
    response_model=UserInvitationResponse,
)
def invite_user(
    company_id: int,
    payload: UserInvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PENDRAGON_ADMIN)
    ),
):
    try:
        _, raw_token = create_user_invitation(
            db,
            company_id=company_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            role=payload.role,
            invited_by_user_id=current_user.id,
        )

    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return UserInvitationResponse(
        message="Invitation created.",
        invitation_token=(
            raw_token
            if settings.environment == "development"
            else None
        ),
    )

@router.get("/invitations")
def list_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PENDRAGON_ADMIN)),
):
    invitations = (
        db.query(UserInvitation)
        .order_by(UserInvitation.created_at.desc())
        .all()
    )

    return [
        {
            "id": invitation.id,
            "company": invitation.company.name,
            "first_name": invitation.first_name,
            "last_name": invitation.last_name,
            "email": invitation.email,
            "role": invitation.role,
            "invited_by": (
                f"{invitation.invited_by_user.first_name} "
                f"{invitation.invited_by_user.last_name}"
            ),
            "email_sent_at": invitation.email_sent_at,
            "expires_at": invitation.expires_at,
            "accepted_at": invitation.accepted_at,
            "invalidated_at": invitation.invalidated_at,
        }
        for invitation in invitations
    ]