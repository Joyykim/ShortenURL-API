import string

from django.http import HttpResponsePermanentRedirect
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from core import throttles
from shorteners.models import Link
from shorteners.serializers import LinkSerializer

words = string.ascii_letters + string.digits


class ShortenerViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_throttles(self):
        if self.action == 'create':
            if self.request.user.is_anonymous:
                return [throttles.AnonThrottle()]
            elif self.request.user.is_membership:
                return [throttles.MembershipThrottle()]
            else:
                return [throttles.UserThrottle()]

    def create(self, request, *args, **kwargs):
        """단축 url 생성"""
        result = super().create(request, *args, **kwargs)
        return Response({'shortURL': result.data['shortURL']}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            serializer.save()
        else:
            serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)


class LinkViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = '_shortURL'
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/url/~ 요청시 realURL 리다이렉트
        ++hits 카운팅
        """
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return HttpResponsePermanentRedirect(redirect_to=serializer.data['realURL'])
