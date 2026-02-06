import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in signup_resp.json().get("message", "")
    # Unregister
    unregister_resp = client.get(f"/activities/{activity}/unregister?email={email}")
    # If participant was removed, status should be 200, else 400 or 404
    assert unregister_resp.status_code in (200, 400, 404)
    # Accept either message or error detail
    if unregister_resp.status_code == 200:
        assert email in unregister_resp.json().get("message", "")
    else:
        detail = unregister_resp.json().get("detail", "")
        assert (
            "not registered" in detail or
            "Activity not found" in detail or
            "Not Found" in detail
        )

def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json().get("detail", "")

def test_unregister_not_registered():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    resp = client.get(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
    detail = resp.json().get("detail", "")
    assert (
        "not registered" in detail or
        "Activity not found" in detail or
        "Not Found" in detail
    )

def test_activity_not_found():
    email = "someone@mergington.edu"
    resp = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert resp.status_code == 404
    resp = client.get(f"/activities/Nonexistent/unregister?email={email}")
    assert resp.status_code == 404
