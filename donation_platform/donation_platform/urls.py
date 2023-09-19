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
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from users.views import UsersListView, UsersCreateView, UsersDetailView, UserSearchView, UserLoginView
from administrator.views import AdministratorListView, AdministratorDetailView, AdministratorSearchView
from moderator.views import ModeratorListView, ModeratorDetailView, ModeratorSearchView
from organization.views import OrganizationListView, OrganizationDetailView, OrganizationSearchView
from articles_states.views import ArticlesStatesListView, ArticlesStatesDetailView
from articles_types.views import ArticlesTypeListView, ArticlesTypeDetailView
from articles_zones.views import ArticlesZonesListView, ArticlesZonesDetailView
from donation.views import DonationListView, DonationDetailView, DonationSearchViewbyUser, DonationSearchViewbyName, DonationSearchViewbyType
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('users/', UsersListView.as_view(), name='user-list'),
    path('users/create/', UsersCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='user-detail'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('administrators/', AdministratorListView.as_view(), name='administrator-list'),
    path('administrators/<int:pk>/', AdministratorDetailView.as_view(), name='administrator-detail'),
    path('administrators/search/', AdministratorSearchView.as_view(), name='administrator-search'),
    path('moderators/', ModeratorListView.as_view(), name='moderator-list'),
    path('moderators/<int:pk>/', ModeratorDetailView.as_view(), name='moderator-detail'),
    path('moderators/search/', ModeratorSearchView.as_view(), name='moderator-search'),
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organizations/search/', OrganizationSearchView.as_view(), name='organization-search'),
    path('articlesstates/', ArticlesStatesListView.as_view(), name='articles-states-list'),
    path('articlesstates/<int:pk>/', ArticlesStatesDetailView.as_view(), name='articles-states-detail'),
    path('articlestypes/', ArticlesTypeListView.as_view(), name='articles-types-list'),
    path('articlestypes/<int:pk>/', ArticlesTypeDetailView.as_view(), name='articles-types-detail'),
    path('articleszones/', ArticlesZonesListView.as_view(), name='articles-zones-list'),
    path('articleszones/<int:pk>/', ArticlesZonesDetailView.as_view(), name='articles-zones-detail'),
    path('donations/', DonationListView.as_view(), name='donations-list'),
    path('donations/<int:pk>/', DonationDetailView.as_view(), name='donations-detail'),
    path('donations/searchbyuser/', DonationSearchViewbyUser.as_view(), name='donations-search-by-user'),
    path('donations/searchbyname/', DonationSearchViewbyName.as_view(), name='donations-search-by-name'),
    path('donations/searchbytype/', DonationSearchViewbyType.as_view(), name='donations-search-by-type'),


    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


