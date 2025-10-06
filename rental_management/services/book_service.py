"""Utility service for book related entity or operation."""

from django.core.exceptions import ValidationError

from rental_management.models.book_model import Book


class BookService:
    """Function service to share book related utility."""

    @classmethod
    def update_book_status(cls, update_book: Book, new_status: str) -> bool:
        """Update book status with the given book record entity and status."""
        try:
            update_book.status = new_status
            update_book.full_clean()
            update_book.save()
        except ValidationError:
            return False
        return True
