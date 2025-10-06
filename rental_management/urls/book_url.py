"""URL routing for book related API endpoints."""

from django.urls import path

from rental_management.views.book.book_viewset import BookViewSet

book_urls = [
    path("list", BookViewSet.as_view({"get": "list"}), name="list-books"),
    path("<int:book_id>", BookViewSet.as_view({"get": "retrieve"}), name="retrieve-book"),
    path("create", BookViewSet.as_view({"post": "create"}), name="create-book"),
    path("update/<int:book_id>", BookViewSet.as_view({"patch": "partial_update"}), name="update-book"),
    path("delete/<int:book_id>", BookViewSet.as_view({"delete": "destroy"}), name="delete-book"),
]
