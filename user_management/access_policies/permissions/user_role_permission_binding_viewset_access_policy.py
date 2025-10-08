"""Access policy statements of user role permission binding CRUD API."""

from typing import TYPE_CHECKING

from rest_access_policy import AccessPolicy
from rest_framework.request import Request

if TYPE_CHECKING:
    from user_management.views.permission.user_role_permission_binding_viewset import UserRolePermissionBindingViewSet


class UserRolePermissionBindingAccessPolicy(AccessPolicy):
    """Access policy defining user role permission binding API permissions.

    Permissions explanation:
    1. Admin users can perform any operation on all role permission assignments.
    2. Normal users such as client accounts can only read row permissions.
    """

    statements = [
        {"action": ["list", "retrieve"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request: Request, view: 'UserRolePermissionBindingViewSet', action: str) -> bool:
        """Override default admin principal with custom admin field."""
        return not request.user.is_anonymous and request.user.is_admin
