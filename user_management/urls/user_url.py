"""URL routing for user related API endpoints."""

from django.urls import path

from user_management.views.user_viewset import UserViewSet

user_urls = [
    path('create', UserViewSet.as_view({'post': 'create'}), name='create-user'),
    path('list', UserViewSet.as_view({'get': 'list'}), name='list-users'),
    path('<int:user_id>', UserViewSet.as_view({'get': 'retrieve'}), name='retrieve-user'),
    path('update/<int:user_id>', UserViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='update-user'),
    path('delete/<int:user_id>', UserViewSet.as_view({'delete': 'destroy'}), name='delete-user'),
]
