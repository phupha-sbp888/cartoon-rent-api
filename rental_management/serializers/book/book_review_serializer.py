"""API model serializer for input and output of book review representation."""

from rest_framework import serializers

from rental_management.models.book_review_model import BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    """Model serializer for book review CRUD operation.

    Validating input and serialize output for book review related endpoints.
    """

    is_recommended = serializers.BooleanField(default=True)

    class Meta:
        """Set up fields for serializing book review model."""

        fields = "__all__"
        model = BookReview
