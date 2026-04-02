import pytest


class TestErrorHandling:
    """Tests for error handling and edge cases using AAA pattern"""

    def test_signup_invalid_activity_name(self, client):
        # Arrange: Use non-existent activity name
        invalid_activity = "NonExistent Club"
        email = "error@mergington.edu"

        # Act: Try to sign up
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )

        # Assert: Should return 404
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_from_invalid_activity_name(self, client):
        # Arrange: Use non-existent activity name
        invalid_activity = "Fake Activity"
        email = "error@mergington.edu"

        # Act: Try to remove
        response = client.delete(
            f"/activities/{invalid_activity}/remove",
            params={"email": email}
        )

        # Assert: Should return 404
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_non_existent_participant(self, client):
        # Arrange: Choose valid activity but email not signed up
        activity_name = "Science Club"
        email = "notsignedup@mergington.edu"

        # Act: Try to remove
        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert: Should return 400
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_signup_missing_email_parameter(self, client):
        # Arrange: Valid activity but missing email
        activity_name = "Gym Class"

        # Act: Try to sign up without email
        response = client.post(
            f"/activities/{activity_name}/signup"
            # No params
        )

        # Assert: Should return 422 (validation error)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_remove_missing_email_parameter(self, client):
        # Arrange: Valid activity but missing email
        activity_name = "Programming Class"

        # Act: Try to remove without email
        response = client.delete(
            f"/activities/{activity_name}/remove"
            # No params
        )

        # Assert: Should return 422 (validation error)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data