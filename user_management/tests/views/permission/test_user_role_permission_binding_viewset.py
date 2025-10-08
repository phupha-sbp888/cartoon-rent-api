"""Unittest scenario for CRUD API of user role permission assignment."""

from typing import Dict, List

from django.urls import reverse
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from user_management.models.user_role_model import UserRole
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import UserRolePermission
from user_management.serializers.permission.user_role_permission_binding_serializer import (
    UserRolePermissionBindingSerializer,
)
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe, normal_user_recipe
from user_management.tests.baker_recipe.user_role_recipe import manager_role_recipe


class TestUserRolePermissionBindingViewSet(APITestCase):
    """Test case for user role permission binding CRUD API."""

    fixtures = ['fixtures/user_role_permission.json']

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        fixture_permissions: UserRolePermission = UserRolePermission.objects.first()
        existing_role: UserRole = manager_role_recipe.make()
        cls.role_permission_binding: UserRolePermissionBinding = Recipe(
            UserRolePermissionBinding, role_id=existing_role, permission_id=fixture_permissions
        ).make()
        cls.admin_user = admin_user_recipe.make()
        cls.normal_user = normal_user_recipe.make()
        cls.user_role: UserRole = existing_role

    def setUp(self) -> None:
        """Login with admin user."""
        self.client.force_authenticate(user=self.admin_user)

    def test_list_user_role_permission_bindings(self) -> None:
        """Test listing all user role permission bindings."""
        url: str = reverse("permission:list-role-permission-bindings")
        expecetd_result: List[UserRolePermissionBindingSerializer] = [
            UserRolePermissionBindingSerializer(self.role_permission_binding).data
        ]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expecetd_result)

    def test_list_user_role_permission_bindings_with_normal_user(self) -> None:
        """Test listing all user role permission bindings with normal user."""
        url: str = reverse("permission:list-role-permission-bindings")
        expecetd_result: List[UserRolePermissionBindingSerializer] = [
            UserRolePermissionBindingSerializer(self.role_permission_binding).data
        ]
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expecetd_result)

    def test_retrieve_user_role_permission_binding(self) -> None:
        """Test retrieving a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:retrieve-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_binding_id'], self.role_permission_binding.permission_binding_id)

    def test_retrieve_non_existing_user_role_permission_binding(self) -> None:
        """Test retrieving user role permission assignment that does not exist."""
        url: str = reverse(
            "permission:retrieve-role-permission-binding", args=[self.role_permission_binding.permission_binding_id + 1]
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_user_role_permission_binding_with_normal_user(self) -> None:
        """Test retrieving a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:retrieve-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_binding_id'], self.role_permission_binding.permission_binding_id)

    def test_create_user_role_permission_binding(self) -> None:
        """Test assigning a new user role permission."""
        url: str = reverse("permission:create-role-permission-binding")
        valid_binding_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 2}
        response: Response = self.client.post(url, data=valid_binding_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role_id'], valid_binding_input['role_id'])
        self.assertEqual(response.data['permission_id'], valid_binding_input['permission_id'])

    def test_create_user_role_permission_binding_with_missing_role(self) -> None:
        """Test assigning a permission to user role with missing role id."""
        url: str = reverse("permission:create-role-permission-binding")
        response: Response = self.client.post(url, data={"permission_id": 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_role_permission_binding_with_missing_permission_id(self) -> None:
        """Test assigning a permission to user role with missing permission id."""
        url: str = reverse("permission:create-role-permission-binding")
        response: Response = self.client.post(url, data={"role_id": self.user_role.role_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_user_role_permission_binding(self) -> None:
        """Test assigning duplicate permission to the same role."""
        url: str = reverse("permission:create-role-permission-binding")
        valid_binding_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 1}
        response: Response = self.client.post(url, data=valid_binding_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_role_permission_binding_with_insufficient_permission(self) -> None:
        """Test assigning a new user role permission."""
        url: str = reverse("permission:create-role-permission-binding")
        valid_binding_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 2}
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.post(url, data=valid_binding_input)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_role_permission_binding(self) -> None:
        """Test updating a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 3}
        response: Response = self.client.put(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_id'], valid_binding_update_input['role_id'])
        self.assertEqual(response.data['permission_id'], valid_binding_update_input['permission_id'])

    def test_update_user_role_permission_binding_with_missing_role(self) -> None:
        """Test updating a permission assignment with missing role id."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.put(url, data={"permission_id": 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_role_permission_binding_with_missing_permission_id(self) -> None:
        """Test updating a permission assignment with missing permission id."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.put(url, data={"role_id": self.user_role.role_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_role_permission_binding_with_insufficient_permission(self) -> None:
        """Test updating a specific user role permission binding by ID with normal user permission."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"role_id": self.user_role.role_id, "permission_id": 3}
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.put(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_user_role_permission_binding(self) -> None:
        """Test partially updating a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"permission_id": 4}
        response: Response = self.client.patch(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_id'], valid_binding_update_input['permission_id'])

    def test_partial_update_user_role_permission_binding_with_insufficient_permission(self) -> None:
        """Test partially updating a specific user role permission binding by ID with normal user permission."""
        url: str = reverse(
            "permission:update-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        valid_binding_update_input: Dict[str, int] = {"permission_id": 4}
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.patch(url, data=valid_binding_update_input)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_role_permission_binding(self) -> None:
        """Test deleting a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:delete-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_role_permission_binding_with_insufficient_permission(self) -> None:
        """Test deleting a specific user role permission binding by ID."""
        url: str = reverse(
            "permission:delete-role-permission-binding", args=[self.role_permission_binding.permission_binding_id]
        )
        self.client.force_authenticate(user=self.normal_user)
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
