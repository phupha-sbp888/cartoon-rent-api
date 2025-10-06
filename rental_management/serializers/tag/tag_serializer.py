"""API model serializer for input and output of tag representation."""

from rest_framework import serializers

from rental_management.models.tag_model import Tag


class TagSerializer(serializers.ModelSerializer):
    """Model serializer for tag CRUD operation.

    Validating input and serialize output for tag related endpoints.
    """

    class Meta:
        """Set up fields for serializing tag model."""

        fields = "__all__"
        model = Tag
