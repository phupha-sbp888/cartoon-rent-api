"""Configuration for storing metadata and settings."""

from django.apps import AppConfig


class RentalManagementConfig(AppConfig):
    """Configuration for rental management app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental_management'
