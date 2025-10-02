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

import os

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

default_api_context_path = os.getenv("API_CONTEXT_PATH", "api/v1/")

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{default_api_context_path}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        f'{default_api_context_path}/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(f'{default_api_context_path}/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
