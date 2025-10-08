"""Model viewset for user role related operations."""

from rest_framework.viewsets import ModelViewSet

from user_management.access_policies.roles.user_role_viewset_access_policy import UserRoleViewSetAccessPolicy
from user_management.models.user_role_model import UserRole
from user_management.serializers.role.user_role_serializer import UserRoleSerializer


class UserRoleViewSet(ModelViewSet):
    """CRUD viewset for user role model.

    Viewset provide the following:
    - GET: list all roles
    - GET (with role id): retrieve a specific role by ID
    - POST: create a new role
    - PUT/PATCH (with role id): update a specific role by ID
    - DELETE (with role id): delete a specific role by ID
    """

    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()
    permission_classes = [UserRoleViewSetAccessPolicy]
    lookup_field = "role_id"
