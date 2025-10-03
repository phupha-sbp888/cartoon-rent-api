"""User role assignment model definition for rental service system."""

from django.db import models

from user_management.models.user_model import User
from user_management.models.user_role_model import UserRole


class UserRoleBinding(models.Model):
    """Model for defining user role bindings."""

    role_binding_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
