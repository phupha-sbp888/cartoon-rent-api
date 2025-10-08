"""Model viewset for assigning user role related operations."""

from django.db.models.query import QuerySet
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework.viewsets import ModelViewSet

from user_management.access_policies.roles.user_role_binding_viewset_access_policy import (
    UserRoleBindingViewSetAccessPolicy,
)
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.serializers.role.user_role_binding_serializer import UserRoleBindingSerializer


class UserRoleBindingViewSet(AccessViewSetMixin, ModelViewSet):
    """CRUD viewset for assigning user role.

    Viewset provide the following:
    - GET: list all role that has been assigned to users
    - GET (with role binding id): retrieve a specific role binding detail by ID
    - POST: assigning a role to a user
    - PUT/PATCH (with role binding id): update a specific role binding by ID
    - DELETE (with role binding id): delete a specific role binding by ID
    """

    serializer_class = UserRoleBindingSerializer
    access_policy = UserRoleBindingViewSetAccessPolicy
    lookup_field = "role_binding_id"

    def get_queryset(self) -> QuerySet:
        """Get scope query records categorized by access policy."""
        return self.access_policy.scope_queryset(self.request, UserRoleBinding.objects.all())
