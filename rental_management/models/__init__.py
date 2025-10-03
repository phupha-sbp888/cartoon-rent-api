"""Rental management models package for model registrations."""

from rental_management.models.book_model import Book
from rental_management.models.book_review_model import BookReview
from rental_management.models.book_tag_binding_model import BookTagBinding
from rental_management.models.rent_history_model import RentHistoryModel
from rental_management.models.tag_model import Tag

__all__ = ["Book", "BookReview", "BookTagBinding", "Tag", "RentHistoryModel"]
