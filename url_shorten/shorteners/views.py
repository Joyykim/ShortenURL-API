from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
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

    # @action(detail=False)
    # def link(self, request, index):
    #     db_id = Link.decode_id(index)
    #     link_db = get_object_or_404(Link, id=db_id)
    #     Link.objects.filter(id=db_id).update(hits=F('hits') + 1)
    #     return redirect(link_db.realURL)

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        short_url = request.build_absolute_uri(result.data['shortURL'])
        return Response({"short_url": short_url})
