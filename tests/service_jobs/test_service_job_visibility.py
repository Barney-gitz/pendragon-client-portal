def test_anonymous_user_cannot_list_service_jobs(client):
    response = client.get("/service-jobs")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated."