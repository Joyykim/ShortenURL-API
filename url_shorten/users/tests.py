from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)

    def test_register(self):
        data = {
            'username': 'admin',
            'password': '1111'
        }
        response = self.client.post('/api/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
