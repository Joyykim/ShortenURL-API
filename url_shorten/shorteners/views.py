from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from shorteners.models import Link
from shorteners.serializers import LinkSerializer

from django.shortcuts import redirect, get_object_or_404
from django.db.models import F
import string

words = string.ascii_letters + string.digits


class ShortenerViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    # lookup_field = 'shortURL'

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     GET /api/url/~ 요청시 realURL 리다이렉트
    #     ++hits 카운팅
    #     """
    #     instance = self.get_object()
    #     instance.hits += 1
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     return HttpResponseRedirect(redirect_to=serializer.data['realURL'])

    def create(self, request, *args, **kwargs):
        """
        단축 url 생성
        """
        result = super().create(request, *args, **kwargs)
        short_url = f"{request.scheme}://{request.get_host()}{request.path}/{result.data['shortURL']}"
        return Response({"short_url": short_url})


class LinkViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'shortURL'
    permission_classes = [AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/url/~ 요청시 realURL 리다이렉트
        ++hits 카운팅
        """
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return HttpResponseRedirect(redirect_to=serializer.data['realURL'])
        # return super().retrieve(request, *args, **kwargs)
