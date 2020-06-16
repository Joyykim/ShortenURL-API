from rest_framework import serializers

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits')
        read_only_fields = ('shortURL',)

    def create(self, validated_data):
        link = super().create(validated_data)
        encoded = self.base62(link.id)
        validated_data['shortURL'] = encoded
        return self.update(link, validated_data)

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result
