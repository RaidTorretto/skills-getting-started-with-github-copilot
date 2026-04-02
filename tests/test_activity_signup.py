import pytest
from src.app import activities


class TestActivitySignupIntegration:
    """Integration tests for signup and removal workflows using AAA pattern"""

    def test_signup_workflow_full_flow(self, client):
        # Arrange: Choose an activity and new email
        activity_name = "Soccer Club"
        email = "integrationtest@mergington.edu"

        # Act: Sign up for the activity
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Signup successful
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

        # Act: Fetch activities to verify in list
        response = client.get("/activities")
        data = response.json()

        # Assert: Activity shows the participant
        assert response.status_code == 200
        assert email in data[activity_name]["participants"]

        # Cleanup: Remove the participant for test isolation
        client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

    def test_duplicate_signup_prevention(self, client):
        # Arrange: Sign up once
        activity_name = "Debate Club"
        email = "duplicate@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act: Try to sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Should fail with 400
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

        # Cleanup
        client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

    def test_capacity_limit_enforcement(self, client):
        # Arrange: Choose an activity with small capacity
        activity_name = "Art Club"  # max_participants: 10
        emails = [f"capacity{i}@mergington.edu" for i in range(11)]  # 11 emails

        # Act: Sign up 10 students (up to capacity)
        for i in range(10):
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": emails[i]}
            )
            assert response.status_code == 200

        # Act: Try to sign up 11th student
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": emails[10]}
        )

        # Assert: Should fail due to capacity (assuming check is implemented)
        # Note: Current implementation may not have capacity check, so this may fail
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        # Cleanup: Remove all added participants
        for email in emails[:10]:
            client.delete(
                f"/activities/{activity_name}/remove",
                params={"email": email}
            )

    def test_removal_workflow_full_flow(self, client):
        # Arrange: Sign up a student
        activity_name = "Drama Club"
        email = "removaltest@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act: Remove the student
        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert: Removal successful
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]

        # Act: Fetch activities to verify removed
        response = client.get("/activities")
        data = response.json()

        # Assert: Participant no longer in list
        assert response.status_code == 200
        assert email not in data[activity_name]["participants"]