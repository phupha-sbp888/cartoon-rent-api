"""Unittest scenario for book related CRUD API."""

from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.enums.book_status_type import BookStatusType
from rental_management.serializers.book.book_serializer import BookSerializer
from rental_management.tests.baker_recipe.book_recipe import available_book_recipe
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe


class TestBookViewSet(APITestCase):
    """Test case for book CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.available_book = available_book_recipe.make()
        cls.admin_user = admin_user_recipe.make()

    def test_create_book(self) -> None:
        """Test creating a new book."""
        url: str = reverse("books:create-book")
        valid_book_input: Dict[str, str] = {
            "name": "test book",
            "status": BookStatusType.AVAILABLE.value,
            "author": "Lorem",
        }
        response: Response = self.client.post(url, data=valid_book_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], valid_book_input["name"])
        self.assertEqual(response.data["status"], valid_book_input["status"])

    def test_create_book_with_empty_name(self) -> None:
        """Test create a new book book with empty name."""
        url: str = reverse("books:create-book")
        invalid_book_input: Dict[str, str] = {"name": "", "status": BookStatusType.AVAILABLE.value, "author": "Lorem"}
        response: Response = self.client.post(url, data=invalid_book_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_missing_name(self) -> None:
        """Test creating book without giving name in request body."""
        url: str = reverse("books:create-book")
        invalid_book_input: Dict[str, str] = {"status": BookStatusType.AVAILABLE.value, "author": "Lorem"}
        response: Response = self.client.post(url, data=invalid_book_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_empty_author(self) -> None:
        """Test creating a new book with empty author."""
        url: str = reverse("books:create-book")
        invalid_book_input: Dict[str, str] = {
            "name": "test book",
            "status": BookStatusType.AVAILABLE.value,
            "author": "",
        }
        response: Response = self.client.post(url, data=invalid_book_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_missing_author(self) -> None:
        """Test creating a new book without giving author name in request body."""
        url: str = reverse("books:create-book")
        invalid_book_input: Dict[str, str] = {
            "name": "test book",
            "status": BookStatusType.AVAILABLE.value,
        }
        response: Response = self.client.post(url, data=invalid_book_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_book(self) -> None:
        """Test listing all books."""
        url: str = reverse("books:list-books")
        expected_result: List[BookSerializer] = [BookSerializer(self.available_book).data]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_book_id(self) -> None:
        """Test getting book information by id."""
        url: str = reverse("books:retrieve-book", args=[self.available_book.book_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book_id"], self.available_book.book_id)

    def test_retrieve_non_existing_book(self) -> None:
        """Test getting book information by id."""
        url: str = reverse("books:retrieve-book", args=[self.available_book.book_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book(self) -> None:
        """Test updating book information by id."""
        url: str = reverse("books:update-book", args=[self.available_book.book_id])
        valid_book_input: Dict[str, str] = {
            "name": "test_update",
            "created_by": self.admin_user.user_id,
            "status": BookStatusType.AVAILABLE.value,
            "author": "Test update author",
        }
        response: Response = self.client.put(url, data=valid_book_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], valid_book_input["name"])
        self.assertEqual(response.data["created_by"], valid_book_input["created_by"])
        self.assertEqual(response.data["status"], valid_book_input["status"])
        self.assertEqual(response.data["author"], valid_book_input["author"])

    def test_partial_update_book(self) -> None:
        """Test partially updating book information by id."""
        url: str = reverse("books:update-book", args=[self.available_book.book_id])
        valid_book_input: Dict[str, str] = {
            "status": BookStatusType.RENTED.value,
        }
        response: Response = self.client.patch(url, data=valid_book_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book_id"], self.available_book.book_id)
        self.assertEqual(response.data["status"], valid_book_input["status"])

    def test_delete_book(self) -> None:
        """Test delete book with ID."""
        url: str = reverse("books:delete-book", args=[self.available_book.book_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
