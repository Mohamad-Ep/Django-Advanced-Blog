"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('accounts.urls', namespace='accounts'), name='accounts'),
    path('blog/', include('blog.urls', namespace='blog'), name='blog'),
    
    path('api-auth/', include('rest_framework.urls')),                  # Basic Auth for DRF
    path('api-docs/', include_docs_urls(title='Api Docs Sample')),      # Api-docs for rest_framework
    
]

# media and static config for development
# if settings.DEBUG:
#     urlpatterns+= static(settings.MEDIA_URL, dosument_root=settings.MEDIA_ROOT)
    
