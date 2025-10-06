"""Unit test for book renting service and history."""

from datetime import datetime
from typing import Dict, Union

from django.urls import reverse
from django.utils import timezone
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.rent_history_model import RentHistoryModel
from rental_management.tests.baker_recipe.book_recipe import available_book_recipe, rented_book_recipe
from user_management.tests.baker_recipe.user_recipe import normal_user_recipe


class TestBookRentViewSet(APITestCase):
    """Test case for renting book and record rent history."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        book_rent_user = normal_user_recipe.make()
        available_book = available_book_recipe.make()
        rented_book = rented_book_recipe.make()
        cls.rent_history = Recipe(
            RentHistoryModel, user_id=book_rent_user, book_id=rented_book, status=RentStatusType.IN_PROGRESS.value
        ).make()
        cls.rented_book = rented_book
        cls.available_book = available_book
        cls.book_rent_user = book_rent_user

    def test_list_book_rent_records(self) -> None:
        """Test listing all book rent records."""
        url: str = reverse("books:list-book-rent")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book_rent_record(self) -> None:
        """Test retrieving book rent record with ID."""
        url: str = reverse("books:retrieve-book-rent", args=[self.rent_history.rent_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rent_id"], self.rent_history.rent_id)
        self.assertEqual(response.data["user_id"], self.book_rent_user.user_id)
        self.assertEqual(response.data["book_id"], self.rented_book.book_id)

    def test_retrieve_non_existing_book_rent_record(self) -> None:
        """Test retrieving nojn existing book rent record with ID."""
        url: str = reverse("books:retrieve-book-rent", args=[self.rent_history.rent_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_rent_record(self) -> None:
        """Test renting book and record the rent history."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user.user_id,
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
            "user_id": self.book_rent_user.user_id,
            "book_id": self.rent_history.book_id,
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
            "book_id": self.rent_history.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_missing_user_id(self) -> None:
        """Test renting book with missing user id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "book_id": self.rent_history.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_rent_record_with_empty_book_id(self) -> None:
        """Test renting book with empty book id."""
        url: str = reverse("books:create-book-rent")
        current_datetime: datetime = timezone.now()
        invalid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user.user_id,
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
            "user_id": self.book_rent_user.user_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        response: Response = self.client.post(url, data=invalid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_rent_record(self) -> None:
        """Test updating book rent record."""
        url: str = reverse("books:update-book-rent", args=[self.rent_history.rent_id])
        current_datetime: datetime = timezone.now()
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {
            "user_id": self.book_rent_user.user_id,
            "book_id": self.available_book.book_id,
            "rented_date": current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": RentStatusType.OVERDUE.value,
        }
        response: Response = self.client.put(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rent_id"], self.rent_history.rent_id)
        self.assertEqual(response.data["status"], RentStatusType.OVERDUE.value)
        self.assertEqual(response.data["user_id"], valid_book_rent_record_input["user_id"])
        self.assertEqual(response.data["book_id"], valid_book_rent_record_input["book_id"])
        self.assertEqual(response.data["rented_date"], valid_book_rent_record_input["rented_date"])

    def test_partial_update_book_rent_record(self) -> None:
        """Test partially updating book rent record."""
        url: str = reverse("books:update-book-rent", args=[self.rent_history.rent_id])
        valid_book_rent_record_input: Dict[str, Union[str, int]] = {"status": RentStatusType.COMPLETED.value}
        response: Response = self.client.patch(url, data=valid_book_rent_record_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rent_id"], self.rent_history.rent_id)
        self.assertEqual(response.data["status"], RentStatusType.COMPLETED.value)
