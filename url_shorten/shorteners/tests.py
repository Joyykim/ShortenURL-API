from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UrlTestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(1, 6):
            data = {'username': f'user{i}', 'password': '1111'}
            self.client.post('/api/users', data=data)

        # user = User.objects.first()
        # data = {'realURL': 'https://www.naver.com/'}
        # self.client.force_authenticate(user=user)
        # response = self.client.post('http://127.0.0.1:8000/api/url', data=data)
        # self.url = response.data['shortURL']

        self.user = User.objects.first()

    def test_shortenURL(self):
        """단축 URL 생성"""
        data = {'realURL': 'https://www.naver.com/'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['shortURL'], data['realURL'])

    def test_redirect(self):
        """URL 리다이렉트"""
        data = {'realURL': 'https://www.naver.com/'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=data)
        response = self.client.get(response.data['shortURL'])

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, data['realURL'])
