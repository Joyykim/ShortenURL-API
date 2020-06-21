from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class GetLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'owner',)
        read_only_fields = fields


class CreateLinkSerializer(serializers.ModelSerializer):
    custom = serializers.CharField(
        max_length=200, required=False, source='_shortURL',
        validators=[UniqueValidator(queryset=Link.objects.all(),
                                    message="이미 존재하는 URL입니다. 다시 입력해 주세요.")])

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'custom', 'is_custom')
        read_only_fields = ('shortURL',)
