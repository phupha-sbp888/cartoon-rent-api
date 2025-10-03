"""URL routing for user roles related API endpoints."""

from django.urls import path

from user_management.views.role.user_role_viewset import UserRoleViewSet

role_urls = [
    path("create", UserRoleViewSet.as_view({'post': 'create'}), name="create-role"),
    path("list", UserRoleViewSet.as_view({'get': 'list'}), name="list-roles"),
    path("<int:role_id>", UserRoleViewSet.as_view({'get': 'retrieve'}), name="retrieve-role"),
    path(
        "update/<int:role_id>",
        UserRoleViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="update-role",
    ),
    path("delete/<int:role_id>", UserRoleViewSet.as_view({'delete': 'destroy'}), name="delete-role"),
]
