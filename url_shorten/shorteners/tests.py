from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UrlTestCase(APITestCase):
    """
    URL 히스토리(list - 자신의 히스토리만)
    멤버쉽 쓰로틀링
    커스텀 URL
    """

    def setUp(self) -> None:
        user = baker.make('users.User')
        self.client.force_authenticate(user=user)
        self.urlData = {'realURL': 'https://www.naver.com/'}

    def test_shortenURL(self):
        """단축 URL 생성"""
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['shortURL'], self.urlData['realURL'])

    def test_redirect(self):
        """URL 리다이렉트"""
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        response = self.client.get(response.data['shortURL'])

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, self.urlData['realURL'])

    def test_(self):
        pass
