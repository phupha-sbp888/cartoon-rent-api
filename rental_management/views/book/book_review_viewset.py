"""Model viewset for book review."""

from typing import Dict, Tuple

from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rental_management.access_policies.book_review_api_access_policy import BookReviewApiAccessPolicy
from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.book_review_model import BookReview
from rental_management.models.rent_history_model import RentHistoryModel
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
    permission_classes = [BookReviewApiAccessPolicy]
    lookup_field = "review_id"

    @transaction.atomic
    def create(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Create a book rent service and update book status.

        User can not review multiple time on a single rent.
        """
        book_review_input_serializer: BookReviewSerializer = self.get_serializer(data=request.data)
        book_review_input_serializer.is_valid(raise_exception=True)

        book_rent_history = len(
            RentHistoryModel.objects.filter(
                user_id=book_review_input_serializer.validated_data["user_id"],
                book_id=book_review_input_serializer.validated_data["book_id"],
                status=RentStatusType.COMPLETED.value,
            )
        )
        book_review_by_user = len(
            self.get_queryset().filter(
                user_id=book_review_input_serializer.validated_data["user_id"],
                book_id=book_review_input_serializer.validated_data["book_id"],
            )
        )
        if book_rent_history == 0 or book_review_by_user == book_rent_history:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={"detail": "Book can be reviewed once per renting."}
            )
        book_review_input_serializer.save()
        return Response(data=book_review_input_serializer.data, status=status.HTTP_201_CREATED)
