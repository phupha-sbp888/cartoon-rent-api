"""Unittest scenario for user manager on creating user."""

from copy import deepcopy

from django.db import IntegrityError
from django.test import TestCase

from user_management.models.user_model import User


class TestUserModel(TestCase):
    """Test case for creating user with custom user model manager function for built-ing django admin command."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.valid_user_create_input = {
            "username": "test_admin_user",
            "password": "test_admin_password",
            "email": "test@email.com",
            "age": 10,
            "first_name": "test",
            "last_name": "admin",
        }

    def test_create_admin_user(self) -> None:
        """Test creating an admin user with custom user model manager."""
        admin_user: User = User.objects.create_superuser(**self.valid_user_create_input)
        self.assertTrue(admin_user.is_admin)
        self.assertEqual(admin_user.username, self.valid_user_create_input["username"])
        self.assertEqual(admin_user.email, self.valid_user_create_input["email"])
        self.assertEqual(admin_user.age, self.valid_user_create_input["age"])
        self.assertEqual(admin_user.first_name, self.valid_user_create_input["first_name"])
        self.assertEqual(admin_user.last_name, self.valid_user_create_input["last_name"])

        # Test creating admin user without username
        invalid_user_input = deepcopy(self.valid_user_create_input)
        invalid_user_input["username"] = ""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(**invalid_user_input)

        # Test creating admin user without password
        invalid_user_input["username"] = "test_admin_user"
        invalid_user_input["password"] = ""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(**invalid_user_input)

        # Test creating admin user with duplicate username
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(**self.valid_user_create_input)

    def test_create_normal_user(self) -> None:
        """Test creating a normal user with custom user model manager."""
        normal_user: User = User.objects.create_user(**self.valid_user_create_input)
        self.assertFalse(normal_user.is_admin)
        self.assertEqual(normal_user.username, self.valid_user_create_input["username"])
        self.assertEqual(normal_user.email, self.valid_user_create_input["email"])
        self.assertEqual(normal_user.age, self.valid_user_create_input["age"])
        self.assertEqual(normal_user.first_name, self.valid_user_create_input["first_name"])
        self.assertEqual(normal_user.last_name, self.valid_user_create_input["last_name"])

        # Test creating a normal user without username
        invalid_user_input = deepcopy(self.valid_user_create_input)
        invalid_user_input["username"] = ""
        with self.assertRaises(ValueError):
            User.objects.create_user(**invalid_user_input)

        # Test creating a normal user without password
        invalid_user_input["username"] = "test_normal_user"
        invalid_user_input["password"] = ""
        with self.assertRaises(ValueError):
            User.objects.create_user(**invalid_user_input)

        # Test creating a normal user with duplicate username
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.valid_user_create_input)
