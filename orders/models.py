from django.db import models
from users.models import User
from products.models import Product
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    



class DailyData(models.Model):
    date = models.DateField(default=timezone.now)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    