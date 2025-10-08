"""Access policy statements of user CRUD API."""

from typing import TYPE_CHECKING

from rest_access_policy import AccessPolicy
from rest_framework.request import Request

if TYPE_CHECKING:
    from user_management.views.user_viewset import UserViewSet


class UserViewSetAccessPolicy(AccessPolicy):
    """Access policy defining user API permissions.

    Permissions explanation:
    1. Admin users can perform any operation on all other users.
    2. Normal users such as client accounts can only view and update their own user information.
    """

    statements = [
        {
            "action": ["update", "partial_update", "retrieve"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_request_own_account",
        },
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request: Request, view: 'UserViewSet', action: str) -> bool:
        """Override default admin principal with custom admin field."""
        return not request.user.is_anonymous and request.user.is_admin

    def is_request_own_account(self, request: Request, view: 'UserViewSet', action: str) -> bool:
        """Check if request user is fetching or updating his own information."""
        query_user = view.get_object()
        return request.user == query_user
