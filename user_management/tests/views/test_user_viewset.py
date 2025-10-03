"""Unittest scenario for CRUD API of user."""

from typing import Dict, Union

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from user_management.models.user_model import User
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe, normal_user_recipe


class TestUserViewSet(APITestCase):
    """Test case for user CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.admin_user: User = admin_user_recipe.make()
        cls.normal_user: User = normal_user_recipe.make()
        cls.valid_user_create_input: Dict[str, Union[str, int]] = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@email.com",
            "age": 5,
            "first_name": "test",
            "last_name": "user",
        }

    def _validate_response_data(self, response: Response, expected_data: Dict[str, Union[bool, str, int]]) -> None:
        """Validate nessesary fields in user response data."""
        self.assertEqual(response.data["username"], expected_data["username"])
        self.assertEqual(response.data["email"], expected_data["email"])
        self.assertEqual(response.data["age"], expected_data["age"])
        self.assertEqual(response.data["first_name"], expected_data["first_name"])
        self.assertEqual(response.data["last_name"], expected_data["last_name"])

    def test_list_users(self) -> None:
        """Test listing all users."""
        url: str = reverse("users:list-users")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user(self) -> None:
        """Test retrieving a specific user by ID."""
        url: str = reverse("users:retrieve-user", args=[self.normal_user.user_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.normal_user.user_id)

        # Test retriving non-existing user
        url: str = reverse("users:retrieve-user", args=[self.normal_user.user_id + self.admin_user.user_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self) -> None:
        """Test creating a new user."""
        url: str = reverse("users:create-user")
        response: Response = self.client.post(url, data=self.valid_user_create_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_response_data(response, self.valid_user_create_input)

    def test_update_user(self) -> None:
        """Test updating a user information with a specific user ID."""
        url: str = reverse("users:update-user", args=[self.normal_user.user_id])
        response: Response = self.client.put(url, data=self.valid_user_create_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_response_data(response, self.valid_user_create_input)

    def test_partial_update_user(self) -> None:
        """Test updating with some given information of a user with a specific user ID."""
        url: str = reverse("users:update-user", args=[self.admin_user.user_id])
        update_user_input: Dict[str, Union[bool, str, int]] = {
            "first_name": "update_first_name",
            "last_name": "updae_last_name",
        }
        response: Response = self.client.patch(url, data=update_user_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], update_user_input["first_name"])
        self.assertEqual(response.data["last_name"], update_user_input["last_name"])

    def test_delete_user(self) -> None:
        """Test deleting the existing user."""
        url: str = reverse("users:delete-user", args=[self.normal_user.user_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(user_id=self.normal_user.user_id).exists())

        # Test deleting non-existing user
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
