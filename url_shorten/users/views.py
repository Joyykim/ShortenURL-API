from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.permissions import IsUserSelf
from users.models import User
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'deactivate':
            return [IsUserSelf()]

        return super().get_permissions()

    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": "failed logout."}, status=status.HTTP_404_NOT_FOUND)

        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        return response

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
