from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activities[activity_name]["participants"] = [email]

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_participant_returns_error():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    activities[activity_name]["participants"] = []

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 404


def test_signup_rejects_non_school_domain():
    activity_name = "Chess Club"
    email = "student@example.com"
    activities[activity_name]["participants"] = []

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert "mergington.edu" in response.json()["detail"]
