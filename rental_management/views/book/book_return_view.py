"""API for returning a rented book."""

from typing import Dict, Optional, Tuple

from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from rental_management.access_policies.book_return_api_access_policy import BookeReturnApiAccessPolicy
from rental_management.enums.book_status_type import BookStatusType
from rental_management.enums.rent_status_type import RentStatusType
from rental_management.models.book_model import Book
from rental_management.models.rent_history_model import RentHistoryModel


@extend_schema(request=None, responses={status.HTTP_204_NO_CONTENT: None})
class BookReturnView(UpdateAPIView):
    """API for return procress od the rented book."""

    queryset = Book.objects.all()
    http_method_names = ["patch"]
    permission_classes = [BookeReturnApiAccessPolicy]
    lookup_field = "book_id"

    @transaction.atomic
    def patch(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Update book status and rent history for returning book into store.

        Steps:
        1. get book record from given book id
        2. get an ongoing rent history of the book with status.
        3. check if the requested book is out of service or is returned already
        4. update book status and rent history of the book
        """
        selected_return_book: Book = self.get_object()
        book_rent_record: Optional[RentHistoryModel] = RentHistoryModel.objects.filter(
            book_id=selected_return_book, status=RentStatusType.IN_PROGRESS.value
        ).first()
        # check if book is already returned or out of service
        if selected_return_book.status == BookStatusType.OUT_OF_SERVICE:
            return Response(data={"detail": "Book is out of service"}, status=status.HTTP_400_BAD_REQUEST)
        if not book_rent_record or selected_return_book.status == BookStatusType.AVAILABLE:
            return Response(data={"detail": "Book is already returned"}, status=status.HTTP_400_BAD_REQUEST)

        # Update book and rent record status
        return_date = timezone.now()
        selected_return_book.status = BookStatusType.AVAILABLE
        book_rent_record.return_date = return_date
        if book_rent_record.status == RentStatusType.OVERDUE or (return_date - book_rent_record.rented_date).days > 7:
            amount_overdue_days = (return_date - book_rent_record.rented_date).days - 7
            late_return_fee = amount_overdue_days * 50
            book_rent_record.status = RentStatusType.UNPAID
            book_rent_record.late_return_fee = late_return_fee
        else:
            book_rent_record.status = RentStatusType.COMPLETED
        selected_return_book.save()
        book_rent_record.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
