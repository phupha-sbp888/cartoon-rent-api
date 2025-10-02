"""User role definition model for rental service system."""

from django.db import models


class UserRole(models.Model):
    """Model for defining user roles."""

    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
