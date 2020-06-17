from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from users.models import User


class UrlTestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(1, 6):
            data = {'username': f'user{i}', 'password': '1111'}
            self.client.post('/api/users', data=data)

        user = User.objects.first()
        data = {'realURL': 'https://www.naver.com/'}
        self.client.force_authenticate(user=user)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=data)
        self.url = response.data['shortURL']
        pass

    def test_redirect(self):
        response = self.client.get(self.url)
        print(response)
