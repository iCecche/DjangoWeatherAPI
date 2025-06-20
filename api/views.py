from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .models import Forecast
from .serializer import ForecastSerializer
from .permissions import IsPremiumOrLimitedUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class ForecastViewSet(ViewSet):
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated, IsPremiumOrLimitedUser]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == "partial_update" or self.action == 'delete':
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [permission() for permission in self.permission_classes]
        
    def list(self, request):
        forecast = Forecast.objects.all()
        if len(forecast) > 0:
            serializer = ForecastSerializer(forecast, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk = None):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        forecast = Forecast.objects.get(pk = pk)
        if forecast:
            serializer = ForecastSerializer(forecast)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ForecastSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        forecast = Forecast.objects.get(pk = pk)
        if forecast:
            serializer = ForecastSerializer(forecast, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk = None):
        forecast = Forecast.objects.get(pk = pk)
        if forecast:
            serializer = ForecastSerializer(forecast, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk = None):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        forecast = Forecast.objects.get(pk = pk)
        if forecast:
            forecast.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes = [IsAuthenticated, IsPremiumOrLimitedUser])
    def by_location(self, request):
        location = request.query_params.get('location')
        if not location:
            return Response({"detail": "Parametro 'location' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        forecasts = Forecast.objects.filter(location =location)
        if forecasts.exists():
            serializer = ForecastSerializer(forecasts, many=True)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsPremiumOrLimitedUser])
    def by_date(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"detail": "Parametro 'date' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        forecasts = Forecast.objects.filter(date=date)
        if forecasts.exists():
            serializer = ForecastSerializer(forecasts, many=True)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)