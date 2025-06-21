from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ViewSet

from .models import Forecast, History
from .serializer import ForecastSerializer, HistorySerializer
from .permissions import IsSuperUser
from rest_framework.permissions import IsAuthenticated, AllowAny
class ForecastViewSet(ViewSet):
    serializer_class = ForecastSerializer
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == "partial_update" or self.action == 'delete':
            return [IsAuthenticated(), IsSuperUser()]
        else:
            return [permission() for permission in self.permission_classes]
        
    def list(self, request):
        forecast = Forecast.objects.all()
        if forecast.exists():
            serializer = ForecastSerializer(forecast, many=True)
            self.saveHistory(request, serializer.data)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk = None):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        forecast = Forecast.objects.filter(pk = pk)
        if forecast.exists():
            serializer = ForecastSerializer(forecast, many=True)
            self.saveHistory(request, serializer.data)
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
        forecast = Forecast.objects.filter(pk = pk)
        if forecast.exists():
            serializer = ForecastSerializer(forecast, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk = None):
        forecast = Forecast.objects.filter(pk = pk)
        if forecast.exists():
            serializer = ForecastSerializer(forecast, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk = None):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        forecast = Forecast.objects.filter(pk = pk)
        if forecast.exists():
            forecast.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes = [IsAuthenticated], throttle_classes=[AnonRateThrottle])
    def by_location(self, request):
        location = request.query_params.get('location')
        if not location:
            return Response({"detail": "Parametro 'location' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        forecasts = Forecast.objects.filter(location =location)
        if forecasts.exists():
            serializer = ForecastSerializer(forecasts, many=True)
            self.saveHistory(request, serializer.data)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], throttle_classes=[AnonRateThrottle])
    def by_date(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"detail": "Parametro 'date' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        forecasts = Forecast.objects.filter(date=date)
        if forecasts.exists():
            serializer = ForecastSerializer(forecasts, many=True)
            self.saveHistory(request, serializer.data)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    def saveHistory(self, request, data):
        if request.user.is_authenticated:
            mapped_data = self.map_data(data, request.user.id)
            history_serializer = HistorySerializer(data=mapped_data)
            if history_serializer.is_valid():
                history_serializer.save()
            else:
                return Response(history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return None

    def map_data(self, forecast_data, user):
        return {
            "forecast_result": forecast_data,
            "user": user
        }

class HistoryViewSet(ViewSet):
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def list(self, request):
        history = History.objects.all()
        if len(history) > 0:
            serializer = ForecastSerializer(history, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_date(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"detail": "Parametro 'date' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        history = History.objects.filter(date=date)
        if history.exists():
            serializer = ForecastSerializer(history, many=True)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_location(self, request):
        location = request.query_params.get('location')
        if not location:
            return Response({"detail": "Parametro 'location' mancante."}, status=status.HTTP_400_BAD_REQUEST)
        history = History.objects.filter(location =location)
        if history.exists():
            serializer = ForecastSerializer(history, many=True)
            return Response(serializer.data)
        return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = HistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk = None):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        history = History.objects.filter(pk = pk)
        if history.exists():
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
