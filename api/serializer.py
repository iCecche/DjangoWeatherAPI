from time import localtime

from rest_framework import serializers
from api.models import Forecast, History


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ["user", 'method', 'endpoint', 'created_on']

    def get_created_on(self, obj):
        return obj.created_at.strftime("%d %b %Y, %H:%M:%S")

    def create(self, validated_data):
        history = History(
            user = validated_data['user'],
            method=validated_data['method'],
            endpoint=validated_data['endpoint']
        )
        history.save()
        return history