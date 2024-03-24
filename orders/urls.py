from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet,OrderItemViewSet,DailyDataViewSet

router = DefaultRouter()
router.register(r'api/v1/orders', OrderViewSet)
router.register(r'api/v1/orders-item', OrderItemViewSet)
router.register(r'api/v1/daily-orders', DailyDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]