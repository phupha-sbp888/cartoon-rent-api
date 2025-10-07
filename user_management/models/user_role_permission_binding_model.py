"""User role permission model definition for rental service system."""

from django.db import models
from django.db.models import UniqueConstraint

from user_management.models.user_role_model import UserRole
from user_management.models.user_role_permission_model import UserRolePermission


class UserRolePermissionBinding(models.Model):
    """Model for assigning user role with permissions."""

    permission_binding_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(UserRolePermission, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Set up unique constraint to prevent duplicate permission assignment and default ordering on query."""

        constraints = [UniqueConstraint(fields=['role_id', 'permission_id'], name='unique_permission_per_role')]
        ordering = ["-created_date"]
