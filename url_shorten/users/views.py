from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        return response

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]

    # 탈퇴 - 비활성화
    @action(detail=False)
    def deactivate(self):
        pass
