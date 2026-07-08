import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def restore_activity_state():
    original_state = {
        activity_name: activity["participants"][:]
        for activity_name, activity in activities.items()
    }

    yield

    for activity_name, participants in original_state.items():
        activities[activity_name]["participants"] = participants
