"""Unittest scenario for CRUD API of user role assignment."""

from typing import Dict

from django.urls import reverse
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from user_management.models.user_model import User
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_model import UserRole
from user_management.tests.baker_recipe.user_recipe import normal_user_recipe
from user_management.tests.baker_recipe.user_role_recipe import client_role_recipe, manager_role_recipe


class TestUserRoleBindingViewSet(APITestCase):
    """Tets case for user role binding CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        existing_role_1: UserRole = manager_role_recipe.make()
        existing_role_2: UserRole = client_role_recipe.make()
        existing_user: User = normal_user_recipe.make()
        cls.role_binding: UserRoleBinding = Recipe(
            UserRoleBinding, user_id=existing_user, role_id=existing_role_1
        ).make()
        cls.role_1: UserRole = existing_role_1
        cls.role_2: UserRole = existing_role_2
        cls.normal_user: User = existing_user

    def test_list_user_role_binding(self) -> None:
        """Test listing all role bindings that are assigned to user."""
        url: str = reverse("roles:list-role-binding")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_user_role_binding(self) -> None:
        """Test retrieving a assigned role to user by ID."""
        url: str = reverse("roles:retrieve-role-binding", args=[self.role_binding.role_binding_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role_binding_id"], self.role_binding.role_binding_id)

    def test_retrieve_non_existing_role_binding(self) -> None:
        """Test retrieving a non existing assigned role to user by ID."""
        url: str = reverse("roles:retrieve-role-binding", args=[self.role_binding.role_binding_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_assigning_role_to_user(self) -> None:
        """Test assigning role to user."""
        url: str = reverse("roles:assign-roles")
        valid_role_assign_input: Dict[str, int] = {"role_id": self.role_2.role_id, "user_id": self.normal_user.user_id}
        response: Response = self.client.post(url, data=valid_role_assign_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role_id"], valid_role_assign_input["role_id"])
        self.assertEqual(response.data["user_id"], valid_role_assign_input["user_id"])

    def test_assigning_duplicate_role_to_user(self) -> None:
        """Test assigning duplicate role to the same user."""
        url: str = reverse("roles:assign-roles")
        valid_role_assign_input: Dict[str, int] = {"role_id": self.role_1.role_id, "user_id": self.normal_user.user_id}
        response: Response = self.client.post(url, data=valid_role_assign_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assigning_role_to_user_with_missing_role_id(self) -> None:
        """Test assigning role without role id."""
        url: str = reverse("roles:assign-roles")
        invalid_role_assign_input: Dict[str, int] = {"user_id": self.normal_user.user_id}
        response: Response = self.client.post(url, data=invalid_role_assign_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assigning_role_to_user_with_missing_user_id(self) -> None:
        """Test assigning role without user id."""
        url: str = reverse("roles:assign-roles")
        invalid_role_assign_input: Dict[str, int] = {
            "role_id": self.role_1.role_id,
        }
        response: Response = self.client.post(url, data=invalid_role_assign_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_role_binding(self) -> None:
        """Test update existing role bindind to user."""
        url: str = reverse("roles:update-role-binding", args=[self.role_binding.role_binding_id])
        valid_role_binding_update_date: Dict[str, int] = {
            "role_id": self.role_2.role_id,
            "user_id": self.normal_user.user_id,
        }
        response: Response = self.client.put(url, data=valid_role_binding_update_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role_id"], valid_role_binding_update_date["role_id"])
        self.assertEqual(response.data["user_id"], valid_role_binding_update_date["user_id"])

    def test_update_role_binding_with_missing_role_id(self) -> None:
        """Test update existing role bindind without role id given."""
        url: str = reverse("roles:update-role-binding", args=[self.role_binding.role_binding_id])
        invalid_role_binding_update_date: Dict[str, int] = {"user_id": self.normal_user.user_id}
        response: Response = self.client.put(url, data=invalid_role_binding_update_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_role_binding_with_missing_user_id(self) -> None:
        """Test update existing role bindind without user id given."""
        url: str = reverse("roles:update-role-binding", args=[self.role_binding.role_binding_id])
        invalid_role_binding_update_date: Dict[str, int] = {"user_id": self.normal_user.user_id}
        response: Response = self.client.put(url, data=invalid_role_binding_update_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_role_binding(self) -> None:
        """Test partial update existing role binding."""
        url: str = reverse("roles:update-role-binding", args=[self.role_binding.role_binding_id])
        valid_role_binding_update_date: Dict[str, int] = {"role_id": self.role_2.role_id}
        response: Response = self.client.patch(url, data=valid_role_binding_update_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role_id"], valid_role_binding_update_date["role_id"])

    def test_delete_user_role_binding(self) -> None:
        """Test delete existing role binding."""
        url: str = reverse("roles:delete-role-binding", args=[self.role_binding.role_binding_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
