"""Access policy for book service CRUD APIs."""

from typing import TYPE_CHECKING

from rest_framework.request import Request

from rental_management.access_policies.global_api_access_policy import GlobalApiAccessPolicy
from rental_management.models.book_review_model import BookReview

if TYPE_CHECKING:
    from rental_management.views.book.book_review_viewset import BookReviewViewSet


class BookReviewApiAccessPolicy(GlobalApiAccessPolicy):
    """Access policy for book service CRUD APIs."""

    statements = [
        {
            "action": ["retrieve", "list", "update", "partial_update", "create"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {"action": ["*"], "principal": "authenticated", "effect": "allow", "condition": "has_role_permission"},
        {"action": ["*"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def has_role_permission(self, request: Request, view: 'BookReviewViewSet', action: str) -> bool:
        """Verify request user permission.

        Check permission in each assigned role or request users request for updating their own reviews.
        """
        if action == "update" or action == "partial_update":
            book_review: BookReview = view.get_object()
            if book_review.user_id == request.user.user_id:
                return True
        return super().has_role_permission(request, view, action)
