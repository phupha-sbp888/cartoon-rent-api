"""API model serializer for output representation of user."""

from rest_framework import serializers

from user_management.models.user_model import User


class UserOutputSerializer(serializers.ModelSerializer):
    """Model serializer for serializng output of user model."""

    class Meta:
        """Set up fields for serializing user model without exposing password through response."""

        model = User
        exclude = ['password']
