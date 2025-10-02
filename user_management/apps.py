"""Configuration for storing metadata and settings."""

from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    """Configuration for user management app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'
