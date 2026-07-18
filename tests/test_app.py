from fastapi.testclient import TestClient

from src.app import app


def test_unregister_participant_removes_the_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]
