"""API model serializer for input and output of book rent record representation."""

from django.db.models import Q
from rest_framework import serializers

from rental_management.enums.book_status_type import BookStatusType
from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.book_model import Book
from rental_management.models.rent_history_model import RentHistoryModel
from user_management.models.user_model import User


class RentHistorySerializer(serializers.ModelSerializer):
    """Model serializer for book rent CRUD operation.

    Validating input and serialize output for book rent related endpoints.
    """

    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        """Set up fields for serializing book rent model."""

        fields = "__all__"
        model = RentHistoryModel

    def validate_book_id(self, validating_book: Book) -> Book:
        """Validate book from book status if the book is currently rented by other users."""
        book_id: int = validating_book.book_id
        if (
            validating_book.status != BookStatusType.AVAILABLE.value
            or RentHistoryModel.objects.filter(Q(book_id=book_id) & ~Q(status=RentStatusType.COMPLETED.value)).exists()
        ):
            raise serializers.ValidationError("The given book ID is already rented.")
        return validating_book
