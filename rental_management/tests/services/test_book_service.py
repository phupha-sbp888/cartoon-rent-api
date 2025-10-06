"""Unittest for book utility service."""

from django.test import TestCase

from rental_management.enums.book_status_type import BookStatusType
from rental_management.services.book_service import BookService
from rental_management.tests.baker_recipe.book_recipe import available_book_recipe


class TestBookService(TestCase):
    """Test case for book service."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.available_book = available_book_recipe.make()

    def test_changing_book_status_with_correct_options(self) -> None:
        """Test changing book status with correct status options defined in model."""
        book_update_result: bool = BookService.update_book_status(
            update_book=self.available_book, new_status=BookStatusType.RENTED
        )
        self.assertTrue(book_update_result)
        self.assertEqual(self.available_book.status, BookStatusType.RENTED.value)

    def test_changing_book_status_with_incorrect_options(self) -> None:
        """Test changing book status with incorrect status options defined in model."""
        book_update_result: bool = BookService.update_book_status(
            update_book=self.available_book, new_status="incorrect status"
        )
        self.assertFalse(book_update_result)
