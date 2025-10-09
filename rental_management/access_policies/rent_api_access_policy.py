"""Access policy for rent service CRUD APIs."""

from typing import List

from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.request import Request

from rental_management.access_policies.global_api_access_policy import GlobalApiAccessPolicy
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import ActionOptions


class RentApiAccessPolicy(GlobalApiAccessPolicy):
    """Access policy for rent service CRUD APIs."""

    statements = [
        {"action": ["retrieve", "list"], "principal": "authenticated", "effect": "allow"},
        {"action": ["*"], "principal": "authenticated", "effect": "allow", "condition": "has_role_permission"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    @classmethod
    def scope_queryset(cls, request: Request, queryset: QuerySet) -> QuerySet:
        """Categorize query output based on request user permission.

        Criteria:
        1. Admin user or user with read all permission: can request for any book rent records.
        2. Normal user: can request for only the records that they are created or assigned to.
        """
        if request.user.is_admin:
            return queryset
        else:
            role_with_read_all_permission: List[int] = list(
                UserRolePermissionBinding.objects.filter(
                    Q(permission_id__action=ActionOptions.READ_ALL.value)
                    | Q(permission_id__action=ActionOptions.ALL.value)
                ).values_list("role_id", flat=True)
            )
            user_assigned_roles_with_read_all_permission = UserRoleBinding.objects.filter(
                user_id=request.user.user_id, role_id__in=role_with_read_all_permission
            )
            if user_assigned_roles_with_read_all_permission.exists():
                return queryset
        return queryset.filter(Q(user_id=request.user.user_id) | Q(created_by=request.user.user_id))
