from rest_framework import serializers

from shorteners.models import Link


class ShotenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('')
