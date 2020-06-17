from rest_framework import serializers

from shorteners.serializers import LinkSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'links')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    # 회원가입 비번 hashing
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
