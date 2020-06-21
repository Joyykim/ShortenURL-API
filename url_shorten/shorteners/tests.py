from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from shorteners.models import Link


class UrlTestCase(APITestCase):
    """
    URL 히스토리(list - 자신의 히스토리만)
    """

    def setUp(self) -> None:
        self.user = baker.make('users.User')
        self.client.force_authenticate(user=self.user)
        self.urlData = {'realURL': 'https://www.naver.com/'}

    def test_shortenURL(self):
        """단축 URL 생성"""
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        response_short_url = response.data['shortURL'].split('/')[-1]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_short_url, self.urlData['realURL'])
        self.assertEqual(len(response_short_url), 6)

    def test_redirect(self):
        """URL 리다이렉트"""
        link = baker.make(Link, realURL=self.urlData['realURL'])
        response = self.client.get(link.shortURL)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, self.urlData['realURL'])
        link = Link.objects.get(realURL=self.urlData['realURL'])
        self.assertEqual(link.hits, 1)

    def test_custom(self):
        """커스텀 url 생성"""
        user = baker.make('users.User', is_membership=True)
        self.client.force_authenticate(user=user)
        url_data = {'realURL': 'https://www.naver.com/', 'custom': 'cucucu', 'is_custom': True}
        response = self.client.post('http://127.0.0.1:8000/api/url', data=url_data)
        response_url = response.data['shortURL'].split('/')[-1]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_url, url_data['custom'])

    def test_custom_duplicated(self):
        """커스텀 url 중복시 사용자에게 재입력 요구"""
        baker.make(Link, realURL='https://www.naver.com/', _shortURL='cucu', is_custom=True)
        url_data = {'realURL': 'https://www.naver.com/', 'custom': 'cucu', 'is_custom': True}
        response = self.client.post('http://127.0.0.1:8000/api/url', data=url_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('custom')[0].code, 'unique')

    def test_throttle_user(self):
        user = baker.make('users.User')
        self.client.force_authenticate(user=user)
        for i in range(20):
            response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttle_membership(self):
        user = baker.make('users.User', is_membership=True)
        self.client.force_authenticate(user=user)
        for i in range(60):
            response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttle_anonymous(self):
        self.client.logout()
        urlData = {'realURL': 'https://www.naver.com/'}
        for i in range(10):
            response = self.client.post('http://127.0.0.1:8000/api/url', data=urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=urlData)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_redirect_10000(self):
        """리다이렉트 요청 10000건"""
        link = baker.make(Link, realURL=self.urlData['realURL'])
        for i in range(1000):
            response = self.client.get(link.shortURL)
            self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        response = self.client.get(link.shortURL)
        # self.assertEqual(response.url, self.urlData['realURL'])
        # link = Link.objects.get(realURL=self.urlData['realURL'])
        # self.assertEqual(link.hits, 1)
