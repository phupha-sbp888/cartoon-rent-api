"""Global access policy for rental service CRUD APIs."""

from typing import Dict, List, Type

from django.db.models import Q
from rest_access_policy import AccessPolicy
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import ActionOptions


class GlobalApiAccessPolicy(AccessPolicy):
    """Global access policy for controlling user access to rental service APIs."""

    statements = [
        {"action": ["retrieve", "list"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "authenticated", "effect": "allow", "condition": "has_role_permission"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request: Request, view: Type[ModelViewSet], action: str) -> bool:
        """Override default admin principal with custom admin field."""
        return not request.user.is_anonymous and request.user.is_admin

    def has_role_permission(self, request: Request, view: Type[ModelViewSet], action: str) -> bool:
        """Verify request user permission by checking permission in each assigned role."""
        permission_action_mapping: Dict[str, str] = {
            "list": ActionOptions.READ_ALL.value,
            "create": ActionOptions.CREATE.value,
            "update": ActionOptions.UPDATE.value,
            "partial_update": ActionOptions.UPDATE.value,
            "destroy": ActionOptions.DELETE.value,
        }
        role_with_selected_permission_action: List[int] = list(
            UserRolePermissionBinding.objects.filter(
                Q(permission_id__action=permission_action_mapping.get(action, ""))
                | Q(permission_id__action=ActionOptions.ALL.value)
            ).values_list("role_id", flat=True)
        )
        user_assigned_roles = UserRoleBinding.objects.filter(
            user_id=request.user.user_id, role_id__in=role_with_selected_permission_action
        )
        return user_assigned_roles.exists()
