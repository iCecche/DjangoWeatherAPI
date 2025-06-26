from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Forecast, History
from .permissions import IsSuperUser
from .serializer import ForecastSerializer, HistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ForecastView(APIView):
    serializer_class = ForecastSerializer
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    def get_permissions(self, action=None):
        if self.request.method in ['post', 'put', 'patch', 'delete']:
            return [IsAuthenticated(), IsSuperUser()]
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        location = request.query_params.get('location')
        date = request.query_params.get('date')
        time = request.query_params.get('time')

        filters = {}
        if location:
            filters['location'] = location
        if date:
            filters['date'] = date
        if time:
            filters['time'] = time

        try:
            forecast = Forecast.objects.filter(**filters)
            serializer = ForecastSerializer(forecast, many=True)
            self.saveHistory(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Forecast.DoesNotExist:
            return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        is_many = isinstance(data, list)
        serializer = ForecastSerializer(data=data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            self.saveHistory(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "ID non fornito."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            forecast = Forecast.objects.get(pk=pk)
            serializer = ForecastSerializer(forecast, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.saveHistory(request)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Forecast.DoesNotExist:
            return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"error:": "ID non fornito."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            forecast = Forecast.objects.get(pk=pk)
            serializer = ForecastSerializer(forecast, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.saveHistory(request)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Forecast.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "ID non fornito"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            forecast = Forecast.objects.get(pk=pk)
            forecast.delete()
            self.saveHistory(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Forecast.DoesNotExist:
            return Response({"detail": "Nessuna previsione trovata."}, status=status.HTTP_404_NOT_FOUND)

    def saveHistory(self, request):
        if request.user.is_authenticated:
            mapped_data = self.map_data(request)
            history_serializer = HistorySerializer(data=mapped_data)
            if history_serializer.is_valid():
                history_serializer.save()

    def map_data(self, request):
        return {
            "user": request.user.id,
            "method": request.method,
            "endpoint": request.path
        }


class HistoryView(APIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        try:
            history = History.objects.filter(user_id=request.user.id)
            serializer = HistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except History.DoesNotExist:
            return Response({"detail": "Nessun record trovato."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = HistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)