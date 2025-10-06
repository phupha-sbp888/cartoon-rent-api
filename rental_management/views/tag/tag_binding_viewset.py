"""Model viewset for book tag assigning model."""

from rest_framework.viewsets import ModelViewSet

from rental_management.models.book_tag_binding_model import BookTagBinding
from rental_management.serializers.tag.tag_binding_serializer import TagBindingSerializer


class TagBindingViewSet(ModelViewSet):
    """CRUD viewset for tag assigning.

    Viewset provide the following:
    - GET: list all available tags that are assigned to book
    - GET (with tag binding id): retrieve a specific tag assigning information
    - POST: assign a tag to book
    - PUT/PATCH (with tag binding id): update a specific tag assignment by ID
    - DELETE (with tag binding id): delete a specific tag assignment by ID
    """

    queryset = BookTagBinding.objects.all()
    serializer_class = TagBindingSerializer
    lookup_field = "book_tag_binding_id"
