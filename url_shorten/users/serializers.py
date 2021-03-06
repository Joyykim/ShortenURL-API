from rest_framework import serializers
from rest_framework.throttling import AnonRateThrottle

from shorteners.serializers import GetLinkSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    links = GetLinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'links')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
