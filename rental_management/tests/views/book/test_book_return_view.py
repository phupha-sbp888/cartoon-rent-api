"""Unit test for book return service."""

import datetime

from django.urls import reverse
from freezegun import freeze_time
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.enums.book_status_type import BookStatusType
from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.rent_history_model import RentHistoryModel
from rental_management.tests.baker_recipe.book_recipe import (
    available_book_recipe,
    out_of_service_book_recipe,
    rented_book_1_recipe,
)
from user_management.models.user_model import User
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_model import UserRole
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import ActionOptions, UserRolePermission
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe, normal_user_recipe, normal_user_recipe_2


class TestBookReturnView(APITestCase):
    """Test case for book return API."""

    fixtures = ['fixtures/user_role_permission.json']

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        role_with_update_permission: UserRole = Recipe(UserRole).make()
        update_permission: UserRolePermission = UserRolePermission.objects.filter(
            action=ActionOptions.UPDATE.value
        ).first()
        Recipe(UserRolePermissionBinding, role_id=role_with_update_permission, permission_id=update_permission).make()
        normal_user_with_update_permission_role: User = normal_user_recipe_2.make()
        Recipe(
            UserRoleBinding, user_id=normal_user_with_update_permission_role, role_id=role_with_update_permission
        ).make()
        cls.normal_user_with_update_permission_role = normal_user_with_update_permission_role
        cls.admin_user = admin_user_recipe.make()
        cls.normal_user_without_role = normal_user_recipe.make()

        rented_book = rented_book_1_recipe.make()
        rented_date = datetime.datetime(2025, 10, 5, 12, 0, 0, tzinfo=datetime.timezone.utc)
        cls.rent_history = Recipe(
            RentHistoryModel, book_id=rented_book, status=RentStatusType.IN_PROGRESS, rented_date=rented_date
        ).make()
        cls.rented_book = rented_book
        cls.available_book = available_book_recipe.make()
        cls.out_of_service_book = out_of_service_book_recipe.make()

    def setUp(self) -> None:
        """Login with admin user."""
        self.client.force_authenticate(user=self.admin_user)

    @freeze_time("2025-10-10 12:00:00")
    def test_return_rented_book_no_penalty(self) -> None:
        """Test returning book without return fee."""
        url = reverse("books:return-book", args=[self.rented_book.book_id])
        response: Response = self.client.patch(url)
        self.rent_history.refresh_from_db()
        self.rented_book.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.rent_history.return_date, datetime.datetime(2025, 10, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(self.rent_history.late_return_fee, 0)
        self.assertEqual(self.rent_history.status, RentStatusType.COMPLETED.value)
        self.assertEqual(self.rented_book.status, BookStatusType.AVAILABLE.value)

    @freeze_time("2025-10-20 12:00:00")
    def test_return_rented_book_with_penalty(self) -> None:
        """Test returning book without return fee."""
        url = reverse("books:return-book", args=[self.rented_book.book_id])
        response: Response = self.client.patch(url)
        self.rent_history.refresh_from_db()
        self.rented_book.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.rent_history.return_date, datetime.datetime(2025, 10, 20, 12, 0, 0, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(self.rent_history.late_return_fee, 400)
        self.assertEqual(self.rent_history.status, RentStatusType.UNPAID.value)
        self.assertEqual(self.rented_book.status, BookStatusType.AVAILABLE.value)

    def test_return_out_of_service_book(self) -> None:
        """Test returning book that is not on operation."""
        url = reverse("books:return-book", args=[self.out_of_service_book.book_id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_available_book(self) -> None:
        """Test returing the book that is not borrowed."""
        url = reverse("books:return-book", args=[self.available_book.book_id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2025-10-10 12:00:00")
    def test_return_book_with_normal_user(self) -> None:
        """Test returning book with user that has update permission."""
        url = reverse("books:return-book", args=[self.rented_book.book_id])
        self.client.force_authenticate(user=self.normal_user_with_update_permission_role)
        response: Response = self.client.patch(url)
        self.rent_history.refresh_from_db()
        self.rented_book.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.rent_history.return_date, datetime.datetime(2025, 10, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(self.rent_history.late_return_fee, 0)
        self.assertEqual(self.rent_history.status, RentStatusType.COMPLETED.value)
        self.assertEqual(self.rented_book.status, BookStatusType.AVAILABLE.value)

    def test_return_book_with_insufficient_permission(self) -> None:
        """Test returning book without permission."""
        url = reverse("books:return-book", args=[self.rented_book.book_id])
        self.client.force_authenticate(user=self.normal_user_without_role)
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
