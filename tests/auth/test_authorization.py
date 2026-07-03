def test_engineer_cannot_invite_users(engineer_client):
    response = engineer_client.post(
        "/companies/1/invitations",
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@example.com",
            "role": "PENDRAGON_ENGINEER",
        },
    )

    assert response.status_code == 403