from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.auth.tokens import generate_token, hash_token
from app.models.user import User
from app.models.user_session import UserSession


SESSION_EXPIRY_DAYS = 7


def create_session(
    db: Session,
    user: User,
) -> tuple[UserSession, str]:
    raw_token = generate_token()
    token_hash = hash_token(raw_token)

    now = datetime.now(timezone.utc)

    session = UserSession(
        user_id=user.id,
        session_token_hash=token_hash,
        expires_at=now + timedelta(days=SESSION_EXPIRY_DAYS),
        revoked_at=None,
    )

    user.last_login_at = now

    db.add(session)
    db.commit()
    db.refresh(session)

    return session, raw_token