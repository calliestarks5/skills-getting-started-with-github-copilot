import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400


def test_unregister_from_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
