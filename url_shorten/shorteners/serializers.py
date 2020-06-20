from rest_framework import serializers

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class LinkSerializer(serializers.ModelSerializer):
    # shortURL = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'owner', 'is_custom')
        read_only_fields = ('shortURL', 'owner')
        extra_kwargs = {
            # 'custom': {'write_only': True},
            'is_custom': {'write_only': True},
        }
