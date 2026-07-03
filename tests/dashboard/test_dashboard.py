from fastapi import status


def test_admin_can_view_dashboard(admin_client):
    response = admin_client.get("/dashboard")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "current_user" in data
    assert "equipment_count" in data
    assert "open_jobs" in data
    assert "completed_jobs" in data
    assert "awaiting_quote" in data


def test_engineer_can_view_dashboard(engineer_client):
    response = engineer_client.get("/dashboard")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "current_user" in data
    assert "equipment_count" in data
    assert "open_jobs" in data
    assert "completed_jobs" in data
    assert "awaiting_quote" in data


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_dashboard_current_user_contains_expected_fields(admin_client):
    response = admin_client.get("/dashboard")

    assert response.status_code == status.HTTP_200_OK

    user = response.json()["current_user"]

    assert user["id"] is not None
    assert user["email"]
    assert user["name"]
    assert user["role"]
    assert user["company"]