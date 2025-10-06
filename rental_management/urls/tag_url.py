"""URL routing for tag related API endpoints."""

from django.urls import path

from rental_management.views.tag.tag_binding_viewset import TagBindingViewSet
from rental_management.views.tag.tag_viewset import TagViewSet

tag_urls = [
    path("list", TagViewSet.as_view({"get": "list"}), name="list-tags"),
    path("<int:tag_id>", TagViewSet.as_view({"get": "retrieve"}), name="retrieve-tag"),
    path("create", TagViewSet.as_view({"post": "create"}), name="create-tag"),
    path("update/<int:tag_id>", TagViewSet.as_view({"put": "update", "patch": "partial_update"}), name="update-tag"),
    path("delete/<int:tag_id>", TagViewSet.as_view({"delete": "destroy"}), name="delete-tag"),
    path("list-binding", TagBindingViewSet.as_view({"get": "list"}), name="list-tag-binding"),
    path("binding/<int:tag_id>", TagBindingViewSet.as_view({"get": "retrieve"}), name="retrieve-tag-binding"),
    path("assign", TagBindingViewSet.as_view({"post": "create"}), name="assign-tags"),
    path(
        "update-binding/<int:tag_id>",
        TagBindingViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="update-tag-binding",
    ),
    path("delete-binding/<int:tag_id>", TagBindingViewSet.as_view({"delete": "destroy"}), name="unassign-tags"),
]
