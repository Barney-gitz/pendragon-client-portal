from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.auth.tokens import generate_token, hash_token
from app.core.exceptions import UserAlreadyExistsError
from app.models.user import User, UserRole
from app.models.user_invitation import UserInvitation


INVITATION_EXPIRY_DAYS = 7


def create_user_invitation(
    db: Session,
    *,
    company_id: int,
    first_name: str,
    last_name: str,
    email: str,
    role: UserRole,
    invited_by_user_id: int,
) -> tuple[UserInvitation, str]:
    normalized_email = email.lower().strip()
    now = datetime.now(timezone.utc)

    existing_user = db.query(User).filter_by(email=normalized_email).first()

    if existing_user is not None:
        raise UserAlreadyExistsError("A user with this email already exists.")

    active_invitations = (
        db.query(UserInvitation)
        .filter(
            UserInvitation.email == normalized_email,
            UserInvitation.accepted_at.is_(None),
            UserInvitation.invalidated_at.is_(None),
        )
        .all()
    )

    for invitation in active_invitations:
        invitation.invalidated_at = now

    raw_token = generate_token()
    token_hash = hash_token(raw_token)

    invitation = UserInvitation(
        company_id=company_id,
        invited_by_user_id=invited_by_user_id,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=normalized_email,
        role=role,
        token_hash=token_hash,
        expires_at=now + timedelta(days=INVITATION_EXPIRY_DAYS),
        email_sent_at=None,
        accepted_at=None,
        invalidated_at=None,
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation, raw_token