from users.models import User,Seller,Buyer
from users.serializers import UserSerializer,SellerSerializer,BuyerSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create associated seller or buyer account based on user role
            if user.role == 'seller':
                # seller_data = {'user': user.id, 'seller_id': 'generate_seller_id_here'}
                # Truncate the username to fit the seller_id field (assuming the username is unique)
                seller_id = user.username[:10]  # Truncate to first 10 characters
                seller_data = {'user': user.id, 'seller_id': seller_id}
                seller_serializer = SellerSerializer(data=seller_data)
                if seller_serializer.is_valid():
                    seller_serializer.save()
                else:
                    user.delete()  # Rollback user creation if failed to create seller account
                    return Response(seller_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif user.role == 'buyer':
                # buyer_data = {'user': user.id, 'buyer_id': 'generate_buyer_id_here'}
                # Truncate the username to fit the seller_id field (assuming the username is unique)
                buyer_id = user.username[:10]  # Truncate to first 10 characters
                buyer_data = {'user': user.id, 'buyer_id': buyer_id}
                buyer_serializer = BuyerSerializer(data=buyer_data)
                if buyer_serializer.is_valid():
                    buyer_serializer.save()
                else:
                    user.delete()  # Rollback user creation if failed to create buyer account
                    return Response(buyer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            if user.role == 'seller':
                try:
                    seller = user.seller_account
                    seller_data = SellerSerializer(seller).data
                    response_data['data'] = seller_data
                    return Response(response_data)
                except Seller.DoesNotExist:
                    return Response({'message': 'User has no seller account'}, status=status.HTTP_404_NOT_FOUND)

            elif user.role == 'buyer':
                try:
                    buyer = user.buyer_account
                    buyer_data = BuyerSerializer(buyer).data
                    response_data['data'] = buyer_data
                    return Response(response_data)
                except Buyer.DoesNotExist:
                    return Response({'message': 'User has no buyer account'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Invalid role'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})    