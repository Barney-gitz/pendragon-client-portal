pytest_plugins = [
    "tests.fixtures.companies",
    "tests.fixtures.users",
    "tests.fixtures.auth",
]

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app
from tests.database import engine


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()


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