import pytest
from src.app import activities


class TestEndpoints:
    """Unit tests for API endpoints using AAA pattern"""

    def test_get_root_redirects_to_static_index(self, client):
        # Arrange: TestClient is provided via fixture

        # Act: Make GET request to root
        response = client.get("/")

        # Assert: Should return the index HTML (redirect followed)
        assert response.status_code == 200
        assert "Mergington High School Activities" in response.text

    def test_get_activities_returns_all_activities(self, client):
        # Arrange: TestClient is provided via fixture

        # Act: Make GET request to activities
        response = client.get("/activities")

        # Assert: Should return 200 and activities dict
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # Based on initial activities
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_signup_for_activity_success(self, client):
        # Arrange: Choose an activity with available spots
        activity_name = "Basketball Team"
        email = "newstudent@mergington.edu"

        # Act: Make POST request to signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Should return 200 and success message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" == data["message"]

        # Verify student was added to participants
        assert email in activities[activity_name]["participants"]

    def test_remove_participant_success(self, client):
        # Arrange: First signup a student
        activity_name = "Art Club"
        email = "removeme@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act: Make DELETE request to remove
        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert: Should return 200 and success message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Removed {email} from {activity_name}" == data["message"]

        # Verify student was removed from participants
        assert email not in activities[activity_name]["participants"]