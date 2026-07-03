import pytest

from app.models.user import UserRole
from tests.factories.user_factory import create_user


@pytest.fixture
def admin_user(db):
    user = create_user(
        email="admin@test.com",
        first_name="Test",
        last_name="Admin",
        role=UserRole.PENDRAGON_ADMIN,
        company_id=1,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user