from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token

from shorteners.views import ShortenerViewSet
from users.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'shorteners', ShortenerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', obtain_auth_token),
]
