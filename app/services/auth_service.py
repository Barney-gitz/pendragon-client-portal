from sqlalchemy.orm import Session

from app.auth.hashing import verify_password
from app.core.exceptions import InvalidCredentialsError
from app.models.user import User
from app.schemas.auth import LoginRequest


def authenticate_user(
    db: Session,
    request: LoginRequest,
) -> User:
    normalized_email = request.email.lower().strip()

    user = (
        db.query(User)
        .filter_by(email=normalized_email)
        .first()
    )

    if user is None:
        raise InvalidCredentialsError("Invalid email or password.")

    if user.password_hash is None:
        raise InvalidCredentialsError("Invalid email or password.")

    if not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password.")

    if not user.is_active:
        raise InvalidCredentialsError("This account is disabled.")

    return user