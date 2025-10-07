"""Unittest scenario for CRUD API of user role."""

from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from user_management.serializers.role.user_role_serializer import UserRoleSerializer
from user_management.tests.baker_recipe.user_role_recipe import manager_role_recipe


class TestUserRoleViewSet(APITestCase):
    """Test case for user role CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.role = manager_role_recipe.make()

    def test_create_user_role(self) -> None:
        """Test creating a new user role."""
        url: str = reverse("roles:create-role")
        valid_role_input: Dict[str, str] = {"name": "Admin", "description": "Administrator role."}
        response: Response = self.client.post(url, data=valid_role_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], valid_role_input['name'])
        self.assertEqual(response.data['description'], valid_role_input['description'])

        #  Test creating a role with an empty name
        response: Response = self.client.post(url, data={"name": "", "description": "No name role."})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #  Test creating a role with a missing name
        response: Response = self.client.post(url, data={"description": "No name role."})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_roles(self) -> None:
        """Test listing all user roles."""
        url: str = reverse("roles:list-roles")
        expected_result: List[UserRoleSerializer] = [UserRoleSerializer(self.role).data]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_user_role(self) -> None:
        """Test retrieving a specific user role by ID."""
        url: str = reverse("roles:retrieve-role", args=[self.role.role_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_id'], self.role.role_id)

    def test_retrieve_non_existing_user_role(self) -> None:
        """Test retrieving a non existing role ID."""
        url: str = reverse("roles:retrieve-role", args=[self.role.role_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_role(self) -> None:
        """Test updating a specific user role by ID."""
        url: str = reverse("roles:update-role", args=[self.role.role_id])
        valid_role_update_input: Dict[str, str] = {"name": "Updated Manager", "description": "Updated description."}
        response: Response = self.client.put(url, data=valid_role_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_role_update_input['name'])
        self.assertEqual(response.data['description'], valid_role_update_input['description'])

        # Test updating a role with an empty name
        response: Response = self.client.put(url, data={"name": "", "description": "Updated description."})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test updating a role with a missing name
        response: Response = self.client.put(url, data={"description": "Updated description."})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_user_role(self) -> None:
        """Test partially updating a specific user role by ID."""
        url: str = reverse("roles:update-role", args=[self.role.role_id])
        valid_role_update_input: Dict[str, str] = {"description": "Partially updated description."}
        response: Response = self.client.patch(url, data=valid_role_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], valid_role_update_input['description'])

    def test_delete_user_role(self) -> None:
        """Test deleting a specific user role by ID."""
        url: str = reverse("roles:delete-role", args=[self.role.role_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
