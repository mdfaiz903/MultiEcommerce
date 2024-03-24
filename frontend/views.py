import requests
from django.shortcuts import render,redirect

# Create your views here.

def HomePage(request):
    response = requests.get('http://127.0.0.1:8000/products/api/v1/products/')
    
    if response.status_code == 200:
        products_list = response.json()
        for product in products_list:
            product['image_url'] = product['image']
    else:
        products_list = []    
    
    context={
        'PRODUCTSLIST' : products_list
    }
    return render(request, 'index.html',context)


def CartPage(request, cart_id):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')  # Assuming you have a form with item_id input
        quantity = request.POST.get('quantity', 1)  # Default quantity is 1 if not provided
        
        # Send a POST request to add the item to the cart via REST API
        response = requests.post(f'http://127.0.0.1:8000/carts/api/v1/carts-item/{cart_id}/add_to_cart/', data={'item_id': item_id, 'quantity': quantity})
        
        if response.status_code == 200:
            # If the item is successfully added to the cart, redirect the user to the cart page
            return redirect('CartPage', cart_id=cart_id)
        else:
            # Handle error response
            # For example, you can display an error message to the user
            error_message = "Failed to add item to cart. Please try again later."
            # You can pass error_message to the template and display it to the user
            
    # If it's a GET request or there's an error, fetch the products list as usual
    response = requests.get(f'http://127.0.0.1:8000/carts/api/v1/carts-item/{cart_id}')
    
    if response.status_code == 200:
        products_list = response.json()
        
        for product in products_list:
            product['image_url'] = product['image']
    else:
        products_list = []    
    
    context = {
        'PRODUCTSLIST': products_list
    }
    return render(request, 'frontend/cart.html', context)




def LoginPage(request):
    return render(request, 'frontend/login.html')


def RegisterPage(request):
    return render(request, 'frontend/register.html')