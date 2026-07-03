from app.auth.hashing import hash_password
from app.models.user import User, UserRole


def create_user(
    *,
    email: str,
    first_name: str,
    last_name: str,
    role: UserRole,
    company_id: int,
) -> User:
    return User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
        company_id=company_id,
        password_hash=hash_password("Password123!"),
        is_active=True,
        is_email_verified=True,
    )