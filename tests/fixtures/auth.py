import pytest


TEST_PASSWORD = "Password123!"


def login_test_user(client, user):
    response = client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200

    return client


@pytest.fixture
def admin_client(client, admin_user):
    return login_test_user(client, admin_user)


@pytest.fixture
def engineer_client(client, engineer_user):
    return login_test_user(client, engineer_user)