
from django.urls import path
from frontend.views import HomePage,CartPage,LoginPage,RegisterPage

urlpatterns = [
    path('', HomePage, name="Home"),
    path('cart/<int:cart_id>/', CartPage, name="CartPage"),
    path('login/', LoginPage, name="LoginPage"),
    path('register/', RegisterPage, name="RegisterPage"),
]
