"""Unittest scenario for CRUD API of tag."""

from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rental_management.serializers.tag.tag_serializer import TagSerializer
from rental_management.tests.baker_recipe.tag_recipe import tag_1_recipe
from user_management.tests.baker_recipe.user_recipe import admin_user_recipe


class TestTagVieSet(APITestCase):
    """Test case for tag CRUD API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.tag = tag_1_recipe.make()
        cls.admin_user = admin_user_recipe.make()

    def test_create_tag(self) -> None:
        """Test creating a new tag."""
        url: str = reverse("tags:create-tag")
        valid_tag_input: Dict[str, str] = {"name": "test"}
        response: Response = self.client.post(url, data=valid_tag_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], valid_tag_input["name"])

    def test_create_tag_with_empty_name(self) -> None:
        """Test creating tag with empty name."""
        url: str = reverse("tags:create-tag")
        invalid_tag_input: Dict[str, str] = {"name": ""}
        response: Response = self.client.post(url, data=invalid_tag_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_with_missing_name(self) -> None:
        """Test creating tag without giving name."""
        url: str = reverse("tags:create-tag")
        response: Response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tag(self) -> None:
        """Test listing all tags."""
        url: str = reverse("tags:list-tags")
        expected_result: List[TagSerializer] = [TagSerializer(self.tag).data]
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], expected_result)

    def test_retrieve_tag_id(self) -> None:
        """Test getting tag information by id."""
        url: str = reverse("tags:retrieve-tag", args=[self.tag.tag_id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tag_id"], self.tag.tag_id)

    def test_retrieve_non_existing_tag(self) -> None:
        """Test getting non existing tag information by id."""
        url: str = reverse("tags:retrieve-tag", args=[self.tag.tag_id + 1])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag(self) -> None:
        """Test updating a tag information by id."""
        url: str = reverse("tags:update-tag", args=[self.tag.tag_id])
        valid_tag_input: Dict[str, str] = {"name": "test_update", "created_by": self.admin_user.user_id}
        response: Response = self.client.put(url, data=valid_tag_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], valid_tag_input["name"])
        self.assertEqual(response.data["created_by"], valid_tag_input["created_by"])

    def test_partial_update_tag(self) -> None:
        """Test partially updating a tag information by id."""
        url: str = reverse("tags:update-tag", args=[self.tag.tag_id])
        valid_tag_input: Dict[str, str] = {"name": "test_update"}
        response: Response = self.client.patch(url, data=valid_tag_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], valid_tag_input["name"])

    def test_delete_tag(self) -> None:
        """Test deleting tag with ID."""
        url: str = reverse("tags:delete-tag", args=[self.tag.tag_id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
