"""Model viewset for tag."""

from rest_framework.viewsets import ModelViewSet

from rental_management.access_policies.tag_api_acces_policy import TagApiAccessPolicy
from rental_management.models.tag_model import Tag
from rental_management.serializers.tag.tag_serializer import TagSerializer


class TagViewSet(ModelViewSet):
    """CRUD viewset for tag.

    Viewset provide the following:
    - GET: list all available tags
    - GET (with tag id): retrieve a specific tag information
    - POST: create a  new tag
    - PUT/PATCH (with tag id): update a specific tag by ID
    - DELETE (with tag id): delete a specific tag by ID
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagApiAccessPolicy]
    lookup_field = "tag_id"
