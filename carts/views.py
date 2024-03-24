from rest_framework import viewsets
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        cart_item = self.get_object()
        quantity = request.data.get('quantity', 1)

        # Update quantity if the cart item already exists
        cart_item.quantity += int(quantity)
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)