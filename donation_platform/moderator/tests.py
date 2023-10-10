import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Users, Moderator, Organization
from users.models import Users


class ModeratorTest(TestCase):
    def setUp(self):
        # Crear un usuario y una organización
        self.users = Users.objects.create(
            user_name="testuser",
            user_password="testpassword",
            user_email="test@example.com",
            user_state=1)

        self.users.save()
        queryset = Users.objects.all()

    # Crear un moderador
        self.moderator_data = {
            'user': self.users.id,
            'start_date': '2023-09-29',
            'moderator_state': 1
        }
        
    def test_create_moderator(self):
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.post('/moderators/', self.moderator_data, format='json')
        self.assertEqual(response.status_code, 201)