from datetime import datetime, timedelta
from decimal import Decimal
from random import randint, choice

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Forecast
from .serializer import ForecastSerializer

# Create your views here.

@api_view(['GET'])
def get_forecast(request):
    return Response(ForecastSerializer(generate_mock_forecast("Florence")).data)

def generate_mock_forecast(location):
    now = datetime.now()
    return Forecast(location=location,
        date=now.date(),
        time=now.time(),
        temperature=Decimal(f"{randint(18, 35)}.{randint(0, 99):02}"),
        description=choice(['Sunny', 'Rainy', 'Cloudy', 'Windy'])
    )