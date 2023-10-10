from datetime import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Users, Administrator, Moderator, Organization
from users.models import Users
from organization.models import Organization


class UsersTest(TestCase):
    def setUp(self):
        # Crea un usuario
        self.users = Users.objects.create(
            user_name="Camila",
            user_email="c@test.classmethod",
            user_password="pwd",
            user_state=1,
        )
        self.users.save()
        queryset = Users.objects.all()
        
        self.organization = Organization.objects.create(
            org_name="Test Organization",
            org_email="test@example.com",
            org_description="Description of test organization",
        )
        self.organization.save()
        queryset = Organization.objects.all()
        
        # Crea un administrador
        self.admin_data = {
            "user": self.users.id,
            "start_date": "2023-09-29",
            "organization_id": self.organization.id,
            "administrator_state": 1,
        }

    def test_create_administrator(self):
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.post("/administrators/", self.admin_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_moderator(self):
        # Create a moderator
        moderator_data = {
            "user": self.users.id,
            "start_date": "2023-09-29",
            "moderator_state": 1,
        }

        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.post("/moderators/", moderator_data, format="json")
        self.assertEqual(response.status_code, 201)


class AdministratorTest(TestCase):
    def setUp(self):
        self.users = Users.objects.create(
            user_name="Camila",
            user_email="c@test.classmethod",
            user_password="pwd",
            user_state=1,
        )
        self.organization = Organization.objects.create(
            org_name="Test Organization",
            org_email="test@example.com",
            org_description="Description of test organization",
        )

    def test_administrator_creation(self):
        administrator = Administrator.objects.create(
            user=self.users,
            start_date="2023-09-29",
            organization_id=self.organization.id,
            administrator_state= 1,
        )

        self.assertEqual(administrator.user, self.users)
        self.assertEqual(administrator.start_date, '2023-09-29')
        # Add more assertions for other fields


class ModeratorTest(TestCase):
    def setUp(self):
        self.users = Users.objects.create(
            user_name="Camila",
            user_email="c@test.classmethod",
            user_password="pwd",
            user_state=1,
        )

    def test_moderator_creation(self):
        moderator = Moderator.objects.create(
            user=self.users, start_date="2023-09-29", moderator_state=1
        )
        self.assertEqual(moderator.user, self.users)
        self.assertEqual(moderator.start_date, "2023-09-29")
        # Add more assertions for other fields
