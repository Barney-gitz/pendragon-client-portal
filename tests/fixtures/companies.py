import pytest

from tests.factories.company_factory import create_company


@pytest.fixture
def company(db):
    company = create_company()

    db.add(company)
    db.commit()
    db.refresh(company)

    return company