import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activity_state():
    original_state = {
        activity_name: activity["participants"][:]
        for activity_name, activity in activities.items()
    }

    yield

    for activity_name, participants in original_state.items():
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
