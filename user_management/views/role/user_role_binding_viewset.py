"""Model viewset for assigning user role related operations."""

from rest_framework.viewsets import ModelViewSet

from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.serializers.role.user_role_binding_serializer import UserRoleBindingSerializer


class UserRoleBindingViewSet(ModelViewSet):
    """CRUD viewset for assigning user role.

    Viewset provide the following:
    - GET: list all role that has been assigned to users
    - GET (with role binding id): retrieve a specific role binding detail by ID
    - POST: assigning a role to a user
    - PUT/PATCH (with role binding id): update a specific role binding by ID
    - DELETE (with role binding id): delete a specific role binding by ID
    """

    queryset = UserRoleBinding.objects.all()
    serializer_class = UserRoleBindingSerializer
    lookup_field = "role_binding_id"
