"""Unittest scenario for CRUD API of user role permission assignment."""

from typing import Dict

from django.urls import reverse
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from user_management.models.user_role_model import UserRole
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import UserRolePermission
from user_management.tests.baker_recipe.user_role_recipe import user_role_recipe


class TestUserRolePermissionBindingViewSet(APITestCase):
    """Test case for user role permission binding CRUD API."""

    fixtures = ['fixtures/user_role_permission.json']

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        fixture_permissions: UserRolePermission = UserRolePermission.objects.first()
        existing_role: UserRole = user_role_recipe.make()
        cls.role_permission_binding: UserRolePermissionBinding = Recipe(
            UserRolePermissionBinding, role_id=existing_role, permission_id=fixture_permissions
        ).make()
        cls.user_role: UserRole = existing_role

    def test_list_user_role_permission_bindings(self) -> None:
        """Test listing all user role permission bindings."""
        url: str = reverse("roles:list-role-permission-bindings")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_user_role_permission_binding(self) -> None:
        """Test retrieving a specific user role permission binding by ID."""
        url: str = reverse(
            "roles:retrieve-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_binding_id'], self.role_permission_binding.permission_binding_id)

        # Test retrieving a non existing binding ID
        url: str = reverse(
            "roles:retrieve-role-permission-binding", args=[self.role_permission_binding.permission_binding_id + 1]
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_role_permission_binding(self) -> None:
        """Test assigning a new user role permission."""
        url: str = reverse("roles:create-role-permission-binding")
        valid_binding_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 2}
        response: Response = self.client.post(url, data=valid_binding_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role_id'], valid_binding_input['role_id'])
        self.assertEqual(response.data['permission_id'], valid_binding_input['permission_id'])

        # Test assigning permission with missing role id
        response: Response = self.client.post(url, data={"permission_id": 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test assigning permission with missing permission id
        response: Response = self.client.post(url, data={"role_id": self.user_role.role_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test assigning duplicate permission to the same role
        response: Response = self.client.post(url, data=valid_binding_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_role_permission_binding(self) -> None:
        """Test updating a specific user role permission binding by ID."""
        url: str = reverse(
            "roles:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 3}
        response: Response = self.client.put(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_id'], valid_binding_update_input['role_id'])
        self.assertEqual(response.data['permission_id'], valid_binding_update_input['permission_id'])

        # Test updating a permission assignment with missing role id
        response: Response = self.client.put(url, data={"permission_id": 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test updating a permission assignment with missing permission id
        response: Response = self.client.put(url, data={"role_id": self.user_role.role_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_user_role_permission_binding(self) -> None:
        """Test partially updating a specific user role permission binding by ID."""
        url: str = reverse(
            "roles:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"permission_id": 4}
        response: Response = self.client.patch(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_id'], valid_binding_update_input['permission_id'])

    def test_delete_user_role_permission_binding(self) -> None:
        """Test deleting a specific user role permission binding by ID."""
        url: str = reverse(
            "roles:delete-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
