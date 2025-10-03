"""Model viewset for user."""

from typing import Dict, Tuple

from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user_management.models.user_model import User
from user_management.serializers.user.user_output_serializer import UserOutputSerializer
from user_management.serializers.user.user_serializer import UserSerializer


@extend_schema_view(
    create=extend_schema(request=UserSerializer, responses={201: UserOutputSerializer}),
    update=extend_schema(request=UserSerializer, responses={200: UserOutputSerializer}),
    partial_update=extend_schema(request=UserSerializer, responses={200: UserOutputSerializer}),
)
class UserViewSet(ModelViewSet):
    """CRUD viewset for user.

    Viewset provide the following:
    - GET: list all users
    - GET (with role id): retrieve a specific user information by ID without password
    - POST: create a new user
    - PUT/PATCH (with role id): update a specific user by ID
    - DELETE (with role id): delete a specific user by ID
    """

    serializer_class = UserOutputSerializer
    queryset = User.objects.all()
    lookup_field = "user_id"

    @transaction.atomic
    def create(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Create a new user and return the created user data without password."""
        input_serializer: UserSerializer = UserSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        new_user: User = input_serializer.save()
        output_serializer: UserOutputSerializer = self.get_serializer(new_user)
        headers: Dict[str, str] = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Update a user information by ID and return the updated user data without password."""
        partial = kwargs.pop('partial', False)
        update_user: User = self.get_object()
        input_serializer: UserSerializer = UserSerializer(update_user, data=request.data, partial=partial)
        input_serializer.is_valid(raise_exception=True)
        updated_user: User = input_serializer.save()

        output_serializer: UserOutputSerializer = self.get_serializer(updated_user)
        return Response(output_serializer.data)
