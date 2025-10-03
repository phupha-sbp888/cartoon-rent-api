"""API model serializer for input representation of user."""

from typing import Any, Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers

from user_management.models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    """Model serializer for serialzing input of user."""

    class Meta:
        """Set up fields for serializing user model for create/update with password."""

        model = User
        fields = "__all__"

    def validate_email(self, raw_email_value: str) -> str:
        """Validate raw email by normalizing email for uppercase email domain.

        For example, customer@EMAIL.com and customer@email.com are the same.
        """
        normalized_email: str = BaseUserManager.normalize_email(raw_email_value)
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("Email is already in use.")
        return normalized_email

    def save(self, **kwargs: Dict[str, Any]) -> User:
        """Save validated data with hash password."""
        if self.validated_data.get('password'):
            self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)
