from rest_framework import serializers

from shorteners.models import Link
import string

words = string.ascii_letters + string.digits


class LinkSerializer(serializers.ModelSerializer):
    shortURL = serializers.SerializerMethodField()
    # owner =

    class Meta:
        model = Link
        fields = ('realURL', 'shortURL', 'hits', 'owner')
        read_only_fields = ('shortURL', 'owner')
        # extra_kwargs = {'owner': {'write_only': True}}

    def create(self, validated_data):
        link = super().create(validated_data)
        encoded = self.base62(link.id)
        link.shortURL = encoded
        link.save()
        return link

    def get_shortURL(self, obj):
        # short_url = f"http:8000//127.0.0.1/api/link/{obj.shortURL}"
        request = self.context['request']
        short_url = f"{request.scheme}://{request.get_host()}/api/link/{obj.shortURL}"
        return short_url

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result
