from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.user import User

from app.auth.tokens import hash_token
from app.core.exceptions import (
    InvalidInvitationError,
    InvitationAlreadyAcceptedError,
    InvitationExpiredError,
    InvitationInvalidatedError,
    PasswordMismatchError,
)
from app.models.user_invitation import UserInvitation
from app.schemas.account_activation import AccountActivationRequest


def activate_account(
    db: Session,
    request: AccountActivationRequest,
):
    if request.password != request.confirm_password:
        raise PasswordMismatchError("Passwords do not match.")

    token_hash = hash_token(request.token)

    invitation = (
        db.query(UserInvitation)
        .filter_by(token_hash=token_hash)
        .first()
    )

    if invitation is None:
        raise InvalidInvitationError("Invitation not found.")

    now = datetime.now(timezone.utc)

    if invitation.invalidated_at is not None:
        raise InvitationInvalidatedError("This invitation has been replaced.")

    if invitation.accepted_at is not None:
        raise InvitationAlreadyAcceptedError(
            "This invitation has already been accepted."
        )

    if invitation.expires_at < now:
        raise InvitationExpiredError("This invitation has expired.")

    password_hash = hash_password(request.password)

    user = User(
        first_name=invitation.first_name,
        last_name=invitation.last_name,
        email=invitation.email,
        password_hash=password_hash,
        company_id=invitation.company_id,
        role=invitation.role,
        is_active=True,
        is_email_verified=True,
        activated_at=now,
    )

    db.add(user)

    invitation.accepted_at = now

    db.commit()

