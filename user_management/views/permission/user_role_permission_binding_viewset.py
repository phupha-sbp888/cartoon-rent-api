"""Model viewset for assigning user role permission related operations."""

from rest_framework.viewsets import ModelViewSet

from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.serializers.permission.user_role_permission_binding_serializer import (
    UserRolePermissionBindingSerializer,
)


class UserRolePermissionBindingViewSet(ModelViewSet):
    """CRUD viewset for assigning user role permission.

    Viewset provide the following:
    - GET: list all role permission that has been assigned
    - GET (with binding id): retrieve a specific role permission binding detail by ID
    - POST: assigning a permission to a role
    - PUT/PATCH (with binding id): update a specific role permission binding by ID
    - DELETE (with binding id): delete a specific role permission binding by ID
    """

    serializer_class = UserRolePermissionBindingSerializer
    queryset = UserRolePermissionBinding.objects.all()
    lookup_field = "permission_binding_id"
