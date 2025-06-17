from django.urls import path
from .views import get_forecast

urlpatterns = [
    path('get_forecast/', get_forecast, name='get_forecast'),
]