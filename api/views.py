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

@api_view(['PUT'])
def update_forecast(request, pk):
    forecast = Forecast.objects.get(id=pk)
    serializer = ForecastSerializer(forecast, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_forecast(request, pk):
    forecast = Forecast.objects.get(id=pk)
    forecast.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)