from django.urls import path
from .views import get_forecast, create_forecast

urlpatterns = [
    path('get_forecast/', get_forecast, name='get_forecast'),
    path('create_forecast/', create_forecast, name='create_forecast'),
]