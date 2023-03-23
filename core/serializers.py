from .models import Zone
from rest_framework import serializers


class ZoneSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = Zone
        fields = ['id','state','title']