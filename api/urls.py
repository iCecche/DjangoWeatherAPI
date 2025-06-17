from django.urls import path
from .views import get_forecast, create_forecast, update_forecast, delete_forecast

urlpatterns = [
    path('get_forecast/', get_forecast, name='get_forecast'),
    path('create_forecast/', create_forecast, name='create_forecast'),
    path('update_forecast/<int:pk>/', update_forecast, name='update_forecast'),
    path('delete_forecast/<int:pk>/', delete_forecast, name='delete_forecast'),
]