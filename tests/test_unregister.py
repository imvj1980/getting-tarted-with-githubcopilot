from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)

original_activity_state = None


def setup_function(function):
    global original_activity_state
    original_activity_state = {
        activity_name: activity["participants"][:]
        for activity_name, activity in activities.items()
    }


def teardown_function(function):
    for activity_name, participants in original_activity_state.items():
        activities[activity_name]["participants"] = participants


def test_unregister_participant_removes_them_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
