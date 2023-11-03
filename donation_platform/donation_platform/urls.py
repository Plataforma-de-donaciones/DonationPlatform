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
from donation.views import DonationListView, DonationDetailView, DonationSearchViewbyUser, DonationSearchViewbyName, DonationSearchViewbyType, DonationSearchViewbyTypeUser, DonationSearchViewbyId
from event.views import EventListView, EventDetailView, EventSearchViewbyUser, EventSearchViewbyName, EventSearchViewbyType
from medical_equipment.views import MedicalEquipmentListView, MedicalEquipmentDetailView, MedicalEquipmentSearchViewbyUser, MedicalEquipmentSearchViewbyName, MedicalEquipmentSearchViewbyType, MedicalEquipmentSearchViewbyTypeUser, MedicalEquipmentSearchViewbyId
from news.views import NewsListView, NewsDetailView, NewsSearchViewbyUser, NewsSearchViewbyName, NewsSearchViewbySubject
from sponsor.views import SponsorListView, SponsorDetailView, SponsorSearchViewbyUser, SponsorSearchViewbyName, SponsorSearchViewbyType, SponsorSearchViewbyTypeUser
from volunteer.views import VolunteerListView, VolunteerDetailView, VolunteerSearchViewbyUser, VolunteerSearchViewbyName, VolunteerSearchViewbyType, VolunteerSearchViewbyTypeUser, VolunteerSearchViewbyId
from notifications.views import NotificationsListView, NotificationsDetailView, NotificationsSearchViewbyUser
from categories_meq.views import CategoriesMeqListView, CategoriesMeqSearchViewByCatId
from categories_don.views import CategoriesDonListView, CategoriesDonSearchViewByCatId
from categories.views import CategoriesListView
from request.views import RequestsListView, RequestsDetailView, RequestsSearchViewbyUser, RequestsSearchViewbyEq, RequestsSearchViewbyDon, RequestsSearchViewbyVol
from conversation.views import ConversationListView, ConversationDetailView, ConversationSearchViewbyUser, ConversationSearchViewbyId
from chat.views import ChatListView, ChatDetailView, ChatSearchViewbyUser, ChatSearchViewbyId, ChatSearchViewbyConversation
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
    path('donations/searchbytypeuser/', DonationSearchViewbyTypeUser.as_view(), name='donations-search-by-type-user'),
    path('donations/searchbyid/', DonationSearchViewbyId.as_view(), name='donation-search-by-id'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/searchbyuser/', EventSearchViewbyUser.as_view(), name='events-search-by-user'),
    path('events/searchbyname/', EventSearchViewbyName.as_view(), name='events-search-by-name'),
    path('events/searchbytype/', EventSearchViewbyType.as_view(), name='events-search-by-type'),
    path('medicalequipments/', MedicalEquipmentListView.as_view(), name='medical-equipment-list'),
    path('medicalequipments/<int:pk>/', MedicalEquipmentDetailView.as_view(), name='medical-equipment-detail'),
    path('medicalequipments/searchbyuser/', MedicalEquipmentSearchViewbyUser.as_view(), name='medical-equipment-search-by-user'),
    path('medicalequipments/searchbyname/', MedicalEquipmentSearchViewbyName.as_view(), name='medical-equipment-search-by-name'),
    path('medicalequipments/searchbytype/', MedicalEquipmentSearchViewbyType.as_view(), name='medical-equipment-search-by-type'),
    path('medicalequipments/searchbytypeuser/', MedicalEquipmentSearchViewbyTypeUser.as_view(), name='medical-equipment-search-by-type-user'),
    path('medicalequipments/searchbyid/', MedicalEquipmentSearchViewbyId.as_view(), name='medical-equipment-search-by-id'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/searchbyuser/', NewsSearchViewbyUser.as_view(), name='news-search-by-user'),
    path('news/searchbyname/', NewsSearchViewbyName.as_view(), name='news-search-by-name'),
    path('news/searchbysubject/', NewsSearchViewbySubject.as_view(), name='news-search-by-subject'),
    path('sponsors/', SponsorListView.as_view(), name='sponsor-list'),
    path('sponsors/<int:pk>/', SponsorDetailView.as_view(), name='sponsor-detail'),
    path('sponsors/searchbyuser/', SponsorSearchViewbyUser.as_view(), name='sponsor-search-by-user'),
    path('sponsors/searchbyname/', SponsorSearchViewbyName.as_view(), name='sponsor-search-by-name'),
    path('sponsors/searchbytype/', SponsorSearchViewbyType.as_view(), name='sponsor-search-by-type'),
    path('sponsors/searchbytypeuser/', SponsorSearchViewbyTypeUser.as_view(), name='sponsor-search-by-type-user'),
    path('volunteers/', VolunteerListView.as_view(), name='volunteer-list'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
    path('volunteers/searchbyuser/', VolunteerSearchViewbyUser.as_view(), name='volunteer-search-by-user'),
    path('volunteers/searchbyname/', VolunteerSearchViewbyName.as_view(), name='volunteer-search-by-name'),
    path('volunteers/searchbytype/', VolunteerSearchViewbyType.as_view(), name='volunteer-search-by-type'),
    path('volunteers/searchbytypeuser/', VolunteerSearchViewbyTypeUser.as_view(), name='volunteer-search-by-type-user'),
    path('volunteers/searchbyid/', VolunteerSearchViewbyId.as_view(), name='volunteer-search-by-id'),
    path('notifications/', NotificationsListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationsDetailView.as_view(), name='notifications-detail'),
    path('notifications/search/', NotificationsSearchViewbyUser.as_view(), name='notifications-search'),
    path('requests/', RequestsListView.as_view(), name='requests-list'),
    path('requests/<int:pk>/', RequestsDetailView.as_view(), name='requests-detail'),
    path('requests/search/', RequestsSearchViewbyUser.as_view(), name='requests-search'),
    path('requests/searchbyeq/', RequestsSearchViewbyEq.as_view(), name='requests-search-eq'),
    path('requests/searchbydon/', RequestsSearchViewbyDon.as_view(), name='requests-search-don'),
    path('requests/searchbyvol/', RequestsSearchViewbyVol.as_view(), name='requests-search-vol'),
    path('categoriesmeq/', CategoriesMeqListView.as_view(), name='categories-meq-list'),
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('categoriesmeq/search/<int:cat_id>/', CategoriesMeqSearchViewByCatId.as_view(), name='categoriesmeq-search-by-cat-id'),
    path('categoriesdon/', CategoriesDonListView.as_view(), name='categories-don-list'),
    path('categoriesdon/search/<int:cat_id>/', CategoriesDonSearchViewByCatId.as_view(), name='categoriesdon-search-by-cat-id'),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/searchbyuser/', ConversationSearchViewbyUser.as_view(), name='conversation-search-by-user'),
    path('conversations/searchbyid/', ConversationSearchViewbyId.as_view(), name='conversation-search-by-id'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chats/searchbyuser/', ChatSearchViewbyUser.as_view(), name='chat-search-by-user'),
    path('chats/searchbyid/', ChatSearchViewbyId.as_view(), name='chat-search-by-id'),
    path('chats/searchbyconv/', ChatSearchViewbyConversation.as_view(), name='chat-search-by-conv'),


    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


