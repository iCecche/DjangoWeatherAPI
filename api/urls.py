
from django.urls import path
from api.views import ForecastView, HistoryView

urlpatterns = [
    path('forecast/', ForecastView.as_view(), name='forecast'),
    path('history/', HistoryView.as_view(), name='history')
]