"""User role permission and action definition for rental service system."""

from django.db import models


class ActionOptions(models.TextChoices):
    """Group permission action for CRUD operations in the system."""

    CREATE = 'CREATE'
    READ_ALL = 'READ_ALL'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    ALL = 'ALL'


class UserRolePermission(models.Model):
    """Model for defining user role permissions."""

    permission_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ActionOptions.choices)
    description = models.TextField(blank=True, null=True)

    class Meta:
        """Set up default ordering on query role permission model."""

        ordering = ["-created_date"]
