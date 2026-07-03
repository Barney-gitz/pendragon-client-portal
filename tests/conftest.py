pytest_plugins = [
    "tests.fixtures.companies",
    "tests.fixtures.users",
]

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from tests.database import TestingSessionLocal


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()