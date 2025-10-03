"""API model serializer for input and output representation of user role permission assignment."""

from rest_framework import serializers

from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding


class UserRolePermissionBindingSerializer(serializers.ModelSerializer):
    """Model serializer for assigning user role permission.

    Validating input and serialize output for assigning user role permission related endpoints.
    """

    class Meta:
        """Set up fields for serializing user role permission binding model."""

        model = UserRolePermissionBinding
        fields = "__all__"
