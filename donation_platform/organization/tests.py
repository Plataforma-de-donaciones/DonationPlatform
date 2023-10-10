from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from test_plus import TestCase
from users.models import Users
from .models import Organization
from colorama import Fore, Back, Style

class OrganizationTest(TestCase):
    def setUp(self):
        self.users = Users.objects.create(
            user_name = 'Camila',
            user_email = 'c@test.classmethod',
            user_password = 'pwd',
            user_state = 1)
        
        self.users.save() 
        queryset = Users.objects.all()
        
        self.org_data = {
            'org_name': '1Test Organization',
            'org_email': '1test@example.com',
            'org_description': '1Description of test organization'
        }
       

    def test_create_organization(self):
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.post('/organizations/', self.org_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_organization_list(self):
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.get('/organizations/')
        self.assertEqual(response.status_code, 200)

    def test_get_organization_detail(self):
        organization = Organization.objects.create(**self.org_data)
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.get(f'/organizations/{organization.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_organization(self):
        organization = Organization.objects.create(**self.org_data)
        updated_data = {
            'org_name': 'Updated Organization Name',
            'org_email': 'updated@example.com',
            'org_description': 'Updated description'
        }
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.put(f'/organizations/{organization.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_organization(self):
        organization = Organization.objects.create(**self.org_data)
        client = APIClient()
        client.force_authenticate(user=self.users)
        response = client.delete(f'/organizations/{organization.id}/')
        self.assertEqual(response.status_code, 204)
