"""Model viewset for book review."""

from rest_framework.viewsets import ModelViewSet

from rental_management.models.book_review_model import BookReview
from rental_management.serializers.book.book_review_serializer import BookReviewSerializer


class BookReviewViewSet(ModelViewSet):
    """CRUD viewset for book review.

    Viewset provide the following:
    - GET: list all book reviews.
    - GET (with book review id): retrieve a specific book review information
    - POST: create a new book review
    - PUT/PATCH (with book review id): update a specific book review by ID
    - DELETE (with book review id): delete a specific book review by ID
    """

    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    lookup_field = "review_id"
