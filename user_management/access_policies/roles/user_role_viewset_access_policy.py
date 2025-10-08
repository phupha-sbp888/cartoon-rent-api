"""Access policy statements of user role CRUD API."""

from typing import TYPE_CHECKING

from rest_access_policy import AccessPolicy
from rest_framework.request import Request

if TYPE_CHECKING:
    from user_management.views.role.user_role_viewset import UserRoleViewSet


class UserRoleViewSetAccessPolicy(AccessPolicy):
    """Access policy defining user API permissions.

    Permissions explanation:
    1. Admin users can perform any operation on all other users.
    2. Normal users such as client accounts can only view and update their own user information.
    """

    statements = [
        {"action": ["list", "retrieve"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request: Request, view: 'UserRoleViewSet', action: str) -> bool:
        """Override default admin principal with custom admin field."""
        return not request.user.is_anonymous and request.user.is_admin
