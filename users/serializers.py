from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User,Seller,Buyer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user




class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')  # Assuming 'user' is an instance of User
        password = user.password
        seller = Seller.objects.create(user=user, **validated_data)
        return seller    

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')  # Assuming 'user' is an instance of User
        password = user.password
        buyer = Buyer.objects.create(user=user, **validated_data)
        return buyer