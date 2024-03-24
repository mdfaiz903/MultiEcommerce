import requests
from django.shortcuts import render

# Create your views here.

def HomePage(request):
    response = requests.get('http://127.0.0.1:8000/products/api/v1/products/')
    
    if response.status_code == 200:
        products_list = response.json()
        for product in products_list:
            product['image_url'] = product['images']
    else:
        products_list = []    
    
    context={
        'PRODUCTSLIST' : products_list
    }
    return render(request, 'index.html',context)


def CartPage(request):
    return render(request, 'frontend/cart.html')



def LoginPage(request):
    return render(request, 'frontend/login.html')


def RegisterPage(request):
    return render(request, 'frontend/register.html')