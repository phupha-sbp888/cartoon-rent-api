"""URL routing for book related API endpoints."""

from django.urls import path

from rental_management.views.book.book_rent_viewset import BookRentViewSet
from rental_management.views.book.book_review_viewset import BookReviewViewSet
from rental_management.views.book.book_viewset import BookViewSet

book_urls = [
    path("list", BookViewSet.as_view({"get": "list"}), name="list-books"),
    path("<int:book_id>", BookViewSet.as_view({"get": "retrieve"}), name="retrieve-book"),
    path("create", BookViewSet.as_view({"post": "create"}), name="create-book"),
    path("update/<int:book_id>", BookViewSet.as_view({"put": "update", "patch": "partial_update"}), name="update-book"),
    path("delete/<int:book_id>", BookViewSet.as_view({"delete": "destroy"}), name="delete-book"),
    path("reviews/list", BookReviewViewSet.as_view({"get": "list"}), name="list-book-reviews"),
    path("reviews/<int:review_id>", BookReviewViewSet.as_view({"get": "retrieve"}), name="retrieve-book-review"),
    path("reviews/create", BookReviewViewSet.as_view({"post": "create"}), name="create-book-review"),
    path(
        "reviews/update/<int:review_id>",
        BookReviewViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="update-book-review",
    ),
    path("reviews/delete/<int:review_id>", BookReviewViewSet.as_view({"delete": "destroy"}), name="delete-book-review"),
    path("rent/list", BookRentViewSet.as_view({"get": "list"}), name="list-book-rent"),
    path("rent/<int:rent_id>", BookRentViewSet.as_view({"get": "retrieve"}), name="retrieve-book-rent"),
    path("rent/create", BookRentViewSet.as_view({"post": "create"}), name="create-book-rent"),
    path(
        "rent/update/<int:rent_id>",
        BookRentViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="update-book-rent",
    ),
    path("rent/delete/<int:rent_id>", BookRentViewSet.as_view({"delete": "destroy"}), name="delete-book-rent"),
]
