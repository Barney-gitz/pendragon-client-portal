from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_session, get_current_user
from app.core.exceptions import InvalidCredentialsError
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import authenticate_user
from app.services.session_service import create_session
from app.models.user_session import UserSession


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, request)

    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    _, raw_session_token = create_session(db, user)

    response.set_cookie(
        key="pendragon_session",
        value=raw_session_token,
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return LoginResponse(message="Login successful.")


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "company_id": current_user.company_id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "is_email_verified": current_user.is_email_verified,
        "activated_at": current_user.activated_at,
        "last_login_at": current_user.last_login_at,
    }

@router.post("/logout")
def logout(
    response: Response,
    current_session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
):
    current_session.revoked_at = datetime.now(timezone.utc)

    db.commit()

    response.delete_cookie(
        key="pendragon_session",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return {"message": "Logged out successfully."}