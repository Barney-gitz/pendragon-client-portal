def test_admin_client_is_authenticated(admin_client):
    response = admin_client.get("/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"