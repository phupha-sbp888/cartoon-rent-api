"""URL routing for user roles related API endpoints."""

from django.urls import path

from user_management.views.role.user_role_permission_binding_viewset import UserRolePermissionBindingViewSet
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
    path(
        "permission/list",
        UserRolePermissionBindingViewSet.as_view({'get': 'list'}),
        name="list-role-permission-bindings",
    ),
    path(
        "permission/assign",
        UserRolePermissionBindingViewSet.as_view({'post': 'create'}),
        name="create-role-permission-binding",
    ),
    path(
        "permission/<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'get': 'retrieve'}),
        name="retrieve-role-permission-binding",
    ),
    path(
        "permission/update/<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="update-role-permission-binding",
    ),
    path(
        "permission/delete/<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'delete': 'destroy'}),
        name="delete-role-permission-binding",
    ),
]
