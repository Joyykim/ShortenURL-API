from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make(User, _quantity=3)
        print(self.users)

    def test_register(self):
        # self.client.force_authenticate(user=self.users[0])
        data = {
            'username': 'admin',
            'password': '1111',
        }
        response = self.client.post('/api/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {
            'username': 'user',
            'password': '1111',
        }
        response = self.client.post('/api/login', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_update_password(self):
        pass
