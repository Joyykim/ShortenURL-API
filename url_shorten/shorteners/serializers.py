from rest_framework import serializers

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class LinkSerializer(serializers.ModelSerializer):
    def get_shortURL(self, obj):
        short_url = f"http:8000//127.0.0.1/api/link/{obj.shortURL}"
        # short_url = f"{request.scheme}://{request.get_host()}{request.path}/{result.data['shortURL']}"

        return short_url

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits')
        read_only_fields = ('_shortURL', 'shortURL')

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
