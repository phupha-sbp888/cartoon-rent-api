"""Model viewset for book."""

from rest_framework.viewsets import ModelViewSet

from rental_management.access_policies.book_api_access_policy import BookApiAccessPolicy
from rental_management.models.book_model import Book
from rental_management.serializers.book.book_serializer import BookSerializer


class BookViewSet(ModelViewSet):
    """CRUD viewset for book.

    Viewset provide the following:
    - GET: list all available books
    - GET (with book id): retrieve a specific book information
    - POST: create a  new book
    - PUT/PATCH (with book id): update a specific book by ID
    - DELETE (with book id): delete a specific book by ID
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [BookApiAccessPolicy]
    lookup_field = "book_id"
