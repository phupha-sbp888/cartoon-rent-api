"""Access policy statements of user role binding CRUD API."""

from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_access_policy import AccessPolicy
from rest_framework.request import Request

if TYPE_CHECKING:
    from user_management.views.role.user_role_binding_viewset import UserRoleBindingViewSet


class UserRoleBindingViewSetAccessPolicy(AccessPolicy):
    """Access policy defining user role binding API permissions.

    Permissions explanation:
    1. Admin users can perform any operation on all role assignments.
    2. Normal users such as client accounts can only view their own role assignment information.
    """

    statements = [
        {"action": ["list", "retrieve"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request: Request, view: 'UserRoleBindingViewSet', action: str) -> bool:
        """Override default admin principal with custom admin field."""
        return not request.user.is_anonymous and request.user.is_admin

    @classmethod
    def scope_queryset(cls, request: Request, queryset: QuerySet) -> QuerySet:
        """Categorize query output based on request user permission.

        Criteria:
        1. Admin user: can request for any role assignment records.
        2. Normal user: can request for only their own records.
        """
        if request.user.is_admin:
            return queryset
        return queryset.filter(user_id=request.user.user_id)
