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

from rental_management.urls.book_url import book_urls
from rental_management.urls.tag_url import tag_urls

tag_base_context_path = "tags/"
book_base_context_path = "books/"

urlpatterns = [
    path(f'{tag_base_context_path}', include((tag_urls, 'tags'), namespace='tags')),
    path(f'{book_base_context_path}', include((book_urls, 'books'), namespace='books')),
]
