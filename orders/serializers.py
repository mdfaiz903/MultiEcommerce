from rest_framework import serializers
from .models import Order,OrderItem,DailyData

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        
        

class DailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyData
        fields = '__all__'                
        
    def save(self,**validate_data):
        daily_data = DailyData.objects.filter(**validate_data)
        print(daily_data,"=============")   
         