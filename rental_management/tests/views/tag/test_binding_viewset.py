"""Unittest scenario for CRUD API of tag assignment."""

from typing import Dict, List

from django.urls import reverse
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.models.book_tag_binding_model import BookTagBinding
from rental_management.serializers.tag.tag_binding_serializer import TagBindingSerializer
from rental_management.tests.baker_recipe.book_recipe import available_book_recipe
from rental_management.tests.baker_recipe.tag_recipe import tag_1_recipe, tag_2_recipe
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe


class TestTagVieSet(APITestCase):
    """Test case for tag assignment CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        tag_1 = tag_1_recipe.make()
        available_book = available_book_recipe.make()
        admin_user = admin_user_recipe.make()
        cls.tag_binding = Recipe(BookTagBinding, book_id=available_book, tag_id=tag_1).make()
        cls.admin_user = admin_user
        cls.tag_1 = tag_1
        cls.tag_2 = tag_2_recipe.make()
        cls.available_book = available_book

    def setUp(self) -> None:
        """Login with admin user."""
        self.client.force_authenticate(user=self.admin_user)

    def test_assign_tag_to_book(self) -> None:
        """Test assigning a tag to book."""
        url: str = reverse("tags:assign-tags")
        valid_tag_assign_input: Dict[str, str] = {"book_id": self.available_book.book_id, "tag_id": self.tag_2.tag_id}
        response: Response = self.client.post(url, data=valid_tag_assign_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book_id"], valid_tag_assign_input["book_id"])
        self.assertEqual(response.data["tag_id"], valid_tag_assign_input["tag_id"])

    def test_assign_duplicate_tag_to_book(self) -> None:
        """Test assigning duplicate tag to a book."""
        url: str = reverse("tags:assign-tags")
        duplicate_tag_assign_input: Dict[str, str] = {
            "book_id": self.available_book.book_id,
            "tag_id": self.tag_1.tag_id,
        }
        response: Response = self.client.post(url, data=duplicate_tag_assign_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tag(self) -> None:
        """Test listing all tag assignment to book."""
        url: str = reverse("tags:list-tag-binding")
        expected_result: List[TagBindingSerializer] = [TagBindingSerializer(self.tag_binding).data]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_tag_binding(self) -> None:
        """Test getting tag assignment information by id."""
        url: str = reverse("tags:retrieve-tag-binding", args=[self.tag_binding.book_tag_binding_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book_tag_binding_id"], self.tag_binding.book_tag_binding_id)

    def test_retrieve_non_existing_tag_binding(self) -> None:
        """Test getting non existing tag assignment information by id."""
        url: str = reverse("tags:retrieve-tag-binding", args=[self.tag_binding.book_tag_binding_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag(self) -> None:
        """Test updating a tag assignment information by id."""
        url: str = reverse("tags:update-tag-binding", args=[self.tag_binding.book_tag_binding_id])
        valid_tag_binding_input: Dict[str, str] = {
            "book_id": self.available_book.book_id,
            "tag_id": self.tag_2.tag_id,
            "created_by": self.admin_user.user_id,
        }
        response: Response = self.client.put(url, data=valid_tag_binding_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book_tag_binding_id"], self.tag_binding.book_tag_binding_id)
        self.assertEqual(response.data["book_id"], valid_tag_binding_input["book_id"])
        self.assertEqual(response.data["tag_id"], valid_tag_binding_input["tag_id"])

    def test_partial_update_tag(self) -> None:
        """Test partially updating a tag assignment information by id."""
        url: str = reverse("tags:update-tag-binding", args=[self.tag_binding.book_tag_binding_id])
        valid_tag_binding_input: Dict[str, str] = {"tag_id": self.tag_2.tag_id}
        response: Response = self.client.patch(url, data=valid_tag_binding_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book_tag_binding_id"], self.tag_binding.book_tag_binding_id)
        self.assertEqual(response.data["tag_id"], valid_tag_binding_input["tag_id"])

    def test_delete_tag(self) -> None:
        """Test deleting tag assignment with ID."""
        url: str = reverse("tags:unassign-tags", args=[self.tag_binding.book_tag_binding_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
