"""Unittest scenario for book review related CRUD API."""

from typing import Dict, List

from django.urls import reverse
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.models.book_review_model import BookReview
from rental_management.serializers.book.book_review_serializer import BookReviewSerializer
from rental_management.tests.baker_recipe.book_recipe import available_book_recipe
from user_management.tests.baker_recipe.user_recipe import normal_user_recipe


class TestBookReviewViewset(APITestCase):
    """Test case for book review CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        book = available_book_recipe.make()
        review_user = normal_user_recipe.make()
        cls.review = Recipe(BookReview, user_id=review_user, book_id=book).make()
        cls.review_user = review_user
        cls.book = book

    def test_create_book_review(self) -> None:
        """Test creating a new book review."""
        url: str = reverse("books:create-book-review")
        valid_review_input: Dict[str, str] = {
            "user_id": self.review_user.user_id,
            "book_id": self.book.book_id,
            "review_detail": "test review detail",
            "is_recommended": True,
        }
        response: Response = self.client.post(url, data=valid_review_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], valid_review_input["user_id"])
        self.assertEqual(response.data["book_id"], valid_review_input["book_id"])
        self.assertTrue(response.data["is_recommended"])

    def test_create_review_with_missing_user_id(self) -> None:
        """Test creating a new book review without giving user id."""
        url: str = reverse("books:create-book-review")
        invalid_review_input: Dict[str, str] = {
            "book_id": self.book.book_id,
            "review_detail": "test review detail",
            "is_recommended": True,
        }
        response: Response = self.client.post(url, data=invalid_review_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_with_missing_book_id(self) -> None:
        """Test creating a new book review without giving book id."""
        url: str = reverse("books:create-book-review")
        invalid_review_input: Dict[str, str] = {
            "user_id": self.review_user.user_id,
            "review_detail": "test review detail",
            "is_recommended": True,
        }
        response: Response = self.client.post(url, data=invalid_review_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_with_missing_review_detail(self) -> None:
        """Test creating a new book review without giving review detail."""
        url: str = reverse("books:create-book-review")
        invalid_review_input: Dict[str, str] = {
            "user_id": self.review_user.user_id,
            "book_id": self.book.book_id,
            "is_recommended": True,
        }
        response: Response = self.client.post(url, data=invalid_review_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reviews(self) -> None:
        """Test listing all book review."""
        url: str = reverse("books:list-book-reviews")
        response: Response = self.client.get(url)
        expected_result: List[BookReviewSerializer] = [BookReviewSerializer(self.review).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_review_from_id(self) -> None:
        """Test getting book review information from id."""
        url: str = reverse("books:retrieve-book-review", args=[self.review.review_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_id"], self.review.review_id)

    def test_retrieve_non_existing_review_from_id(self) -> None:
        """Test getting non existing book review information from id."""
        url: str = reverse("books:retrieve-book-review", args=[self.review.review_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book_review(self) -> None:
        """Test updating book review information by id."""
        url: str = reverse("books:update-book-review", args=[self.review.review_id])
        valid_review_update_input: Dict[str, str] = {
            "user_id": self.review_user.user_id,
            "book_id": self.book.book_id,
            "is_recommended": False,
            "review_detail": "updated ereview detail",
        }
        response: Response = self.client.put(url, data=valid_review_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_id"], self.review.review_id)
        self.assertEqual(response.data["user_id"], valid_review_update_input["user_id"])
        self.assertEqual(response.data["book_id"], valid_review_update_input["book_id"])
        self.assertFalse(response.data["is_recommended"])

    def test_partial_update_book_review(self) -> None:
        """Test partially updating book review information by id."""
        url: str = reverse("books:update-book-review", args=[self.review.review_id])
        valid_review_update_input: Dict[str, str] = {"is_recommended": False, "review_detail": "updated ereview detail"}
        response: Response = self.client.patch(url, data=valid_review_update_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_id"], self.review.review_id)
        self.assertFalse(response.data["is_recommended"])

    def test_delete_book_review(self) -> None:
        """Test delete book review information by id."""
        url: str = reverse("books:delete-book-review", args=[self.review.review_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
