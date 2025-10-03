"""Model for recording book rent history of the store."""

from django.core.validators import MinValueValidator
from django.db import models

from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.book_model import Book
from user_management.models.user_model import User


class RentHistoryModel(models.Model):
    """Model defining the history record of each book rent."""

    rent_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="rent_user_id")
    rented_date = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=RentStatusType.choices, default=RentStatusType.IN_PROGRESS)
    return_date = models.DateTimeField(null=True, blank=True)
    late_return_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0, "Late penalty fee can not be negative")],
    )
