"""URL routing for user roles related API endpoints."""

from django.urls import path

from user_management.views.permission.user_role_permission_binding_viewset import UserRolePermissionBindingViewSet

permission_urls = [
    path(
        "list",
        UserRolePermissionBindingViewSet.as_view({'get': 'list'}),
        name="list-role-permission-bindings",
    ),
    path(
        "assign",
        UserRolePermissionBindingViewSet.as_view({'post': 'create'}),
        name="create-role-permission-binding",
    ),
    path(
        "<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'get': 'retrieve'}),
        name="retrieve-role-permission-binding",
    ),
    path(
        "update/<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="update-role-permission-binding",
    ),
    path(
        "delete/<int:permission_binding_id>",
        UserRolePermissionBindingViewSet.as_view({'delete': 'destroy'}),
        name="delete-role-permission-binding",
    ),
]
