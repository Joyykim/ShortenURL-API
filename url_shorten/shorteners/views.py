from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from shorteners.models import Shotener


class ShortenerViewSet(viewsets.ModelViewSet):
    queryset = Shotener.objects.all()
    # serializer_class =
