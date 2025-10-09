"""Model viewset for book rent."""

from typing import Dict, Tuple

from django.db import transaction
from django.db.models import QuerySet
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rental_management.access_policies.rent_api_access_policy import RentApiAccessPolicy
from rental_management.enums.book_status_type import BookStatusType
from rental_management.models.rent_history_model import RentHistoryModel
from rental_management.serializers.book.rent_history_serializer import RentHistorySerializer
from rental_management.services.book_service import BookService


class BookRentViewSet(AccessViewSetMixin, ModelViewSet):
    """CRUD viewset for book rent service.

    Viewset provide the following:
    - GET: list all book rent history.
    - GET (with rent id): retrieve a specific book rent information
    - POST: create a new book review
    - PUT/PATCH (with rent id): update a specific book rent by ID
    - DELETE (with book rent id): delete a specific book rent by ID
    """

    serializer_class = RentHistorySerializer
    access_policy = RentApiAccessPolicy
    lookup_field = "rent_id"

    @transaction.atomic
    def create(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Create a book rent service and update book status."""
        rent_information_input_serializer: RentHistorySerializer = self.get_serializer(data=request.data)
        rent_information_input_serializer.is_valid(raise_exception=True)

        # Update book status from available to rented book
        book_update_status: bool = BookService.update_book_status(
            update_book=rent_information_input_serializer.validated_data["book_id"],
            new_status=BookStatusType.RENTED.value,
        )
        if not book_update_status:
            return Response(
                data={"detail": "Can not update book status. Please contact admin."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        rent_information_input_serializer.save()
        return Response(data=rent_information_input_serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet:
        """Get scope query records categorized by access policy."""
        return self.access_policy.scope_queryset(self.request, RentHistoryModel.objects.all())
