"""
URL configuration for go_truth project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views  # Import views from the blog app
from blog.views import register, auth_logout  # Import the register view
from django.contrib.auth import views as auth_views  # Import auth_views for authentication views

from django.contrib.auth.views import LogoutView  # Import LogoutView for logout functionality

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



