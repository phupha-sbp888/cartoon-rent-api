"""Access policy for book return service CRUD APIs."""

from typing import TYPE_CHECKING, List

from django.db.models import Q
from rest_framework.request import Request

from rental_management.access_policies.global_api_access_policy import GlobalApiAccessPolicy
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import ActionOptions

if TYPE_CHECKING:
    from rental_management.views.book.book_return_view import BookReturnView


class BookeReturnApiAccessPolicy(GlobalApiAccessPolicy):
    """Access policy for book return service CRUD APIs."""

    statements = [
        {"action": ["*"], "principal": "authenticated", "effect": "allow", "condition": "has_role_permission"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def has_role_permission(self, request: Request, view: 'BookReturnView', action: str) -> bool:
        """Verify request user has update permission or all type permission to call book return API."""
        role_with_selected_permission_action: List[int] = list(
            UserRolePermissionBinding.objects.filter(
                Q(permission_id__action=ActionOptions.UPDATE.value) | Q(permission_id__action=ActionOptions.ALL.value)
            ).values_list("role_id", flat=True)
        )
        user_assigned_roles = UserRoleBinding.objects.filter(
            user_id=request.user.user_id, role_id__in=role_with_selected_permission_action
        )
        return user_assigned_roles.exists()
