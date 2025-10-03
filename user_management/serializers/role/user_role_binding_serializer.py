"""API model serializer for input and output representation of user role assignment."""

from rest_framework import serializers

from user_management.models.user_role_binding_model import UserRoleBinding


class UserRoleBindingSerializer(serializers.ModelSerializer):
    """Model serializer for assigning user role.

    Validating input and serialize output for assigning user role related endpoints.
    """

    class Meta:
        """Set up fields for serializing user role binding model."""

        model = UserRoleBinding
        fields = "__all__"
