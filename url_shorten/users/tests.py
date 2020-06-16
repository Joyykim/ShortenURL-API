from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

# User = get_user_model()
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'admin',
            'password': '1111',
        }
        self.client.post('/api/users', data=self.data)
        self.user = User.objects.first()

    def test_register(self):
        data = {
            'username': 'user1',
            'password': '1111',
        }
        response = self.client.post('/api/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/login', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)

    def test_update_password(self):
        pass
