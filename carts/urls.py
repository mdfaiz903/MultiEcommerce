from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'api/v1/carts-item', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]