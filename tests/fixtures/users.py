import pytest

from app.models.user import UserRole
from tests.factories.user_factory import create_user


@pytest.fixture
def admin_user(db, company):
    user = create_user(
        email="admin@test.com",
        first_name="Test",
        last_name="Admin",
        role=UserRole.PENDRAGON_ADMIN,
        company_id=company.id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def engineer_user(db, company):
    user = create_user(
        email="engineer@test.com",
        first_name="Test",
        last_name="Engineer",
        role=UserRole.PENDRAGON_ENGINEER,
        company_id=company.id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user