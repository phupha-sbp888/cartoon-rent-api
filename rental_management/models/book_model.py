"""Book model definition for rental service system."""

from django.db import models

from rental_management.enums.book_status_type import BookStatusType
from user_management.models.user_model import User


class Book(models.Model):
    """Model for defining book entity."""

    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BookStatusType.choices, default=BookStatusType.AVAILABLE)
    author = models.CharField(max_length=255, null=False, blank=False)
