"""API model serializer for input and output of book representation."""

from rest_framework import serializers

from rental_management.models.book_model import Book


class BookSerializer(serializers.ModelSerializer):
    """Model serializer for book CRUD operation.

    Validating input and serialize output for book related endpoints.
    """

    class Meta:
        """Set up fields for serializing book model."""

        fields = "__all__"
        model = Book
