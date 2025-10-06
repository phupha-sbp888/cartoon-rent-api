"""API model serializer for input and output of tag assigning representation."""

from rest_framework import serializers

from rental_management.models.book_tag_binding_model import BookTagBinding


class TagBindingSerializer(serializers.ModelSerializer):
    """Model serializer for tag assigning CRUD operation.

    Validating input and serialize output for tag assigning related endpoints.
    """

    class Meta:
        """Set up fields for serializing tag assigning model."""

        fields = "__all__"
        model = BookTagBinding
