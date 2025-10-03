"""URL routing for user roles related API endpoints."""

from django.urls import path

from user_management.views.role.user_role_binding_viewset import UserRoleBindingViewSet
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
    path("list-binding", UserRoleBindingViewSet.as_view({'get': 'list'}), name="list-role-binding"),
    path("assign", UserRoleBindingViewSet.as_view({'post': 'create'}), name="assign-roles"),
    path(
        "binding/<int:role_binding_id>",
        UserRoleBindingViewSet.as_view({'get': 'retrieve'}),
        name="retrieve-role-binding",
    ),
    path(
        "update-binding/<int:role_binding_id>",
        UserRoleBindingViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="update-role-binding",
    ),
    path(
        "delete-binding/<int:role_binding_id>",
        UserRoleBindingViewSet.as_view({'delete': 'destroy'}),
        name="update-role-binding",
    ),
]
