from fastapi import APIRouter

from app.db.session import SessionLocal
from app.models.company import Company

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("")
def list_companies():
    session = SessionLocal()

    try:
        companies = session.query(Company).order_by(Company.name).all()

        return [
            {
                "id": company.id,
                "name": company.name,
                "is_active": company.is_active,
            }
            for company in companies
        ]

    finally:
        session.close()