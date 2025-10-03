"""
URL configuration for cartoon_rent_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

from user_management.urls.permissions_url import permission_urls
from user_management.urls.role_url import role_urls
from user_management.urls.user_url import user_urls

role_base_context_path = "roles/"
user_base_context_path = "users/"
permission_base_context_path = "permission/"

urlpatterns = [
    path(f'{role_base_context_path}', include((role_urls, 'roles'), namespace='roles')),
    path(f'{permission_base_context_path}', include((permission_urls, 'permission'), namespace='permission')),
    path(f'{user_base_context_path}', include((user_urls, 'users'), namespace='users')),
]
