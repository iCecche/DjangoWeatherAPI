from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Forecast
from .serializer import ForecastSerializer

# Create your views here.

@api_view(['GET'])
def get_forecast(request):
    forecasts = Forecast.objects.all()
    serializer = ForecastSerializer(forecasts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_forecast(request):
    serializer = ForecastSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)