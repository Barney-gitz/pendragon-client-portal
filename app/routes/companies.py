from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.company import Company
from app.schemas.company import CompanyResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get(
    "",
    response_model=list[CompanyResponse],
)
def list_companies(db: Session = Depends(get_db)):
    companies = (
        db.query(Company)
        .order_by(Company.name)
        .all()
    )

    return companies