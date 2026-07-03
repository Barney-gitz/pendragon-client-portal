from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.tokens import hash_token
from app.db.session import get_db
from app.models.user import User
from app.models.user_session import UserSession


SESSION_COOKIE_NAME = "pendragon_session"


def get_current_session(
    request: Request,
    db: Session = Depends(get_db),
) -> UserSession:
    raw_session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if raw_session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )

    session_token_hash = hash_token(raw_session_token)

    session = (
        db.query(UserSession)
        .filter(UserSession.session_token_hash == session_token_hash)
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session.",
        )

    if session.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session revoked.",
        )

    now = datetime.now(timezone.utc)

    if session.expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired.",
        )

    return session


def get_current_user(
    current_session: UserSession = Depends(get_current_session),
) -> User:
    return current_session.user