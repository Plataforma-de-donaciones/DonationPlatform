"""donation_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from donation_platform import settings
from users.views import UsersListView, UsersCreateView, UsersDetailView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('users/', UsersListView.as_view(), name='user-list'),
    path('users/create/', UsersCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='user-detail'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)