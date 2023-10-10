from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Administrator
from users.models import Users

class AdminTest(TestCase):
    def setUp(self):
        # Crea un usuario
        self.users = Users.objects.create(
            user_name = 'Camila',
            user_email = 'c@test.classmethod',
            user_password = 'pwd',
            user_state = 1)

        #print(self.users.id)
        self.users.save()
        #print(self.users.id)
        
        queryset = Users.objects.all()
       # for user in queryset:
        #    print(f"ID: {user.id}, Nombre de usuario: {user.user_name}")

        # Crea un administrador
        self.admin_data = {
            'user': self.users.id,
            'start_date': '2023-09-29',
            'organization_id': 1,
            'administrator_state': 1
        }

    def test_create_administrator(self):
        client = APIClient()
        client.force_authenticate(user=self.users)
        #print(self.admin_data)
        # response = client.post('/users/create', self.admin_data, format='json')
        response = client.post('/administrators/', self.admin_data, format='json')
        #print("Response data:", response.data)
        #print("Response content:", response.content)
        self.assertEqual(response.status_code, 201)