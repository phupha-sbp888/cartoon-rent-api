"""User model definition for rental service system."""

from typing import Dict, Union

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models


class BookUserManager(BaseUserManager):
    """Custom user manager for handling user creation."""

    def _create_user(self, username: str, password: str, **extra_fields: Dict[str, Union[str, int]]) -> 'User':
        """Create and save a user with the given username, password, and other information according to User model."""
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str, **extra_fields: Dict[str, Union[str, int]]) -> 'User':
        """Create a normal user for the system."""
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username: str, password: str, **extra_fields: Dict[str, Union[str, int]]) -> 'User':
        """Create an admin user for the system using django built-in command line."""
        extra_fields.setdefault('is_admin', True)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """Model for defining users to be used for rental system authentication and user management API."""

    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Age can not be less than 1")], null=False, blank=False
    )
    created_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'age', 'first_name', 'last_name']

    objects = BookUserManager()

    class Meta:
        """Set up default ordering on query user model."""

        ordering = ["-created_date"]
