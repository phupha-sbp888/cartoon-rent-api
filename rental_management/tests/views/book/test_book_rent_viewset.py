"""Unit test for book renting service and history."""

from datetime import datetime
from typing import Dict, List, Union

from django.urls import reverse
from django.utils import timezone
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.book_model import Book
from rental_management.models.rent_history_model import RentHistoryModel
from rental_management.serializers.book.rent_history_serializer import RentHistorySerializer
from rental_management.tests.baker_recipe.book_recipe import (
    available_book_recipe,
    rented_book_1_recipe,
    rented_book_2_recipe,
)
from user_management.models.user_role_binding_model import UserRoleBinding
from user_management.models.user_role_model import UserRole
from user_management.models.user_role_permission_binding_model import UserRolePermissionBinding
from user_management.models.user_role_permission_model import ActionOptions, UserRolePermission
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe, normal_user_recipe, normal_user_recipe_2


class TestBookRentViewSet(APITestCase):
    """Test case for renting book and record rent history."""

    fixtures = ['fixtures/user_role_permission.json']

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        book_rent_user_1 = normal_user_recipe.make()
        book_rent_user_2 = normal_user_recipe_2.make()
        role_with_read_all_permission: UserRole = Recipe(UserRole).make()
        read_all_permission: UserRolePermission = UserRolePermission.objects.filter(
            action=ActionOptions.READ_ALL.value
        ).first()
        Recipe(
            UserRolePermissionBinding, role_id=role_with_read_all_permission, permission_id=read_all_permission
        ).make()
        Recipe(UserRoleBinding, user_id=book_rent_user_2, role_id=role_with_read_all_permission).make()

        available_book = available_book_recipe.make()
        rented_book_1 = rented_book_1_recipe.make()
        rented_book_2 = rented_book_2_recipe.make()
        cls.rent_history_1 = Recipe(
            RentHistoryModel, user_id=book_rent_user_1, book_id=rented_book_1, status=RentStatusType.UNPAID.value
        ).make()
        cls.rent_history_2 = Recipe(
            RentHistoryModel, user_id=book_rent_user_2, book_id=rented_book_2, status=RentStatusType.IN_PROGRESS.value
        ).make()
        cls.rented_book_1 = rented_book_1
        cls.available_book = available_book
        cls.book_rent_user_1 = book_rent_user_1
        cls.book_rent_user_2 = book_rent_user_2
        cls.unverify_book_record = Recipe(Book, name="").make()
        cls.admin_user = admin_user_recipe.make()

    def setUp(self) -> None:
        """Login with admin user."""
        self.client.force_authenticate(user=self.admin_user)

    def test_list_book_rent_records(self) -> None:
        """Test listing all book rent records."""
        url: str = reverse("books:list-book-rent")
        expected_result: List[RentHistorySerializer] = [
            RentHistorySerializer(self.rent_history_2).data,
            RentHistorySerializer(self.rent_history_1).data,
        ]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"], expected_result)

    def test_list_book_rent_records_with_normal_user(self) -> None:
        """Test listing all book rent records with normal user that does not have read all permission."""
        url: str = reverse("books:list-book-rent")
        expected_result: List[RentHistorySerializer] = [RentHistorySerializer(self.rent_history_1).data]
        self.client.force_authenticate(user=self.book_rent_user_1)
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_list_book_rent_records_with_read_all_permission(self) -> None:
        """Test listing all book rent records with normal user that have read all permission."""
        url: str = reverse("books:list-book-rent")
        expected_result: List[RentHistorySerializer] = [
            RentHistorySerializer(self.rent_history_2).data,
            RentHistorySerializer(self.rent_history_1).data,
        ]
        self.client.force_authenticate(user=self.book_rent_user_2)
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_book_rent_record(self) -> None:
        """Test retrieving book rent record with ID."""
        url: str = reverse("books:retrieve-book-rent", args=[self.rent_history_1.rent_id])
        expected_result: RentHistorySerializer = RentHistorySerializer(self.rent_history_1).data
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)

    def test_retrieve_non_existing_book_rent_record(self) -> None:
        """Test retrieving nojn existing book rent record with ID."""
        url: str = reverse(
            "books:retrieve-book-rent", args=[self.rent_history_1.rent_id + self.rent_history_2.rent_id + 1]
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_rent_record(self) -> None:
        """Test renting book and record the rent history."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_2.user_id,
            "book_id": self.available_book.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], RentStatusType.IN_PROGRESS.value)
        self.assertEqual(response.data["user_id"], valid_book_rent_record_input["user_id"])
        self.assertEqual(response.data["book_id"], valid_book_rent_record_input["book_id"])
        self.assertEqual(response.data["rented_date"], valid_book_rent_record_input["rented_date"])

    def test_create_rented_book_rent_record(self) -> None:
        """Test renting book that is currently been borrowed by other users and record the rent history."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_1.user_id,
            "book_id": self.rent_history_1.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_empty_user_id(self) -> None:
        """Test renting book with empty user id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": "",
            "book_id": self.rent_history_1.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_missing_user_id(self) -> None:
        """Test renting book with missing user id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "book_id": self.rent_history_1.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_empty_book_id(self) -> None:
        """Test renting book with empty book id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_1.user_id,
            "book_id": "",
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_missing_book_id(self) -> None:
        """Test renting book without giving book id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_1.user_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_unverify_book_record(self) -> None:
        """Test renting book with invalid field on book record."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_2.user_id,
            "book_id": self.unverify_book_record.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_book_rent_record_with_unpaid_late_fee(self) -> None:
        """Test renting book with user that has unpaid rent record."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_1.user_id,
            "book_id": self.unverify_book_record.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_rent_record(self) -> None:
        """Test updating book rent record."""
        url: str = reverse("books:update-book-rent", args=[self.rent_history_1.rent_id])
        current_datetime: datetime = timezone.now()
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user_1.user_id,
            "book_id": self.available_book.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": RentStatusType.OVERDUE.value,
        }
        response: Response = self.client.put(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rent_id"], self.rent_history_1.rent_id)
        self.assertEqual(response.data["status"], RentStatusType.OVERDUE.value)
        self.assertEqual(response.data["user_id"], valid_book_rent_record_input["user_id"])
        self.assertEqual(response.data["book_id"], valid_book_rent_record_input["book_id"])
        self.assertEqual(response.data["rented_date"], valid_book_rent_record_input["rented_date"])

    def test_partial_update_book_rent_record(self) -> None:
        """Test partially updating book rent record."""
        url: str = reverse("books:update-book-rent", args=[self.rent_history_1.rent_id])
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {"status": RentStatusType.COMPLETED.value}
        response: Response = self.client.patch(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rent_id"], self.rent_history_1.rent_id)
        self.assertEqual(response.data["status"], RentStatusType.COMPLETED.value)
