
from rest_framework.routers import DefaultRouter
from .views import BrokerViewSet

router = DefaultRouter()
router.register(r'', BrokerViewSet, basename='broker')

urlpatterns = router.urls