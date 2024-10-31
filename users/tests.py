from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user(self):
        data = {
            "user": {
                "username": "test_user",
                "email": "test@test.com",
                "cpf": "12345678909",
                "password": "test123"
            },
            "type_user": {
                "type": "people"
            }
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, 201)
