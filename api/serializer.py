from rest_framework import serializers
from api.models import Forecast, History


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ["user", 'forecast_result']

    def create(self, validated_data):
        history = History(
            user = validated_data['user'],
            forecast_result = validated_data['forecast_result']
        )
        history.save()
        return history