"""API model serializer for input and output representation of user roles."""

from rest_framework import serializers

from user_management.models.user_role_model import UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    """Model serializer for user role model validating input and serialize output for role related endpoints."""

    class Meta:
        """Set up fields for serializing user role model."""

        model = UserRole
        fields = "__all__"
