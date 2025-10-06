"""Book client review model for rental service system."""

from django.db import models

from rental_management.models.book_model import Book
from user_management.models.user_model import User


class BookReview(models.Model):
    """Model for defining book review entity."""

    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_detail = models.TextField(null=False, blank=False)
    is_recommended = models.BooleanField(default=False)
