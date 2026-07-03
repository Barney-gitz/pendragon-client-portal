from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidInvitationError,
    InvitationAlreadyAcceptedError,
    InvitationExpiredError,
    InvitationInvalidatedError,
    PasswordMismatchError,
)
from app.db.session import get_db
from app.schemas.account_activation import (
    AccountActivationRequest,
    AccountActivationResponse,
)
from app.services.account_activation_service import activate_account

router = APIRouter(
    prefix="/invitations",
    tags=["account activation"],
)

@router.post(
    "/accept",
    response_model=AccountActivationResponse,
)
def accept_invitation(
    request: AccountActivationRequest,
    db: Session = Depends(get_db),
):
    try:
        activate_account(
            db=db,
            request=request,
        )

    except PasswordMismatchError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except InvalidInvitationError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    except (
        InvitationExpiredError,
        InvitationAlreadyAcceptedError,
        InvitationInvalidatedError,
    ) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AccountActivationResponse(
        message="Account activated successfully."
    )