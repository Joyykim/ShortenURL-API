from rest_framework import serializers

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class GetLinkSerializer(serializers.ModelSerializer):
    # shortURL = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'owner',)
        read_only_fields = fields


class CreateLinkSerializer(serializers.ModelSerializer):
    custom = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'custom', 'is_custom')
        read_only_fields = ('shortURL',)
        # extra_kwargs = {}

    def run_validation(self, data=empty):
        return super().run_validation(data)

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception)

    def create(self, validated_data):
        """custom 검증 후"""
        if validated_data.get('is_custom'):
            validated_data['_shortURL'] = validated_data['custom']
            validated_data.pop('custom')
        return super().create(validated_data)
