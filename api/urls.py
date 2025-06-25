from rest_framework.routers import DefaultRouter
from .views import ForecastViewSet, HistoryViewSet

router = DefaultRouter()
router.register(r'forecast', ForecastViewSet, basename='forecast')
router.register(r'history', HistoryViewSet, basename='history')
urlpatterns = router.urls