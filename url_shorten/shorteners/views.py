from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action

from shorteners.models import Link
from shorteners.serializers import ShotenerSerializer

from django.shortcuts import redirect, get_object_or_404
from django.db.models import F


class ShortenerViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = ShotenerSerializer

    @action(detail=False)
    def link(request, id):
        db_id = Link.deocde_id(id)
        link_db = get_object_or_404(Link, id=db_id)
        Link.objects.filter(id=db_id).update(hits=F('hits') + 1)
        return redirect(link_db.link)
