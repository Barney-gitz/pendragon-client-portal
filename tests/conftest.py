import pytest
from fastapi.testclient import TestClient

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
def client():
    return TestClient(app)