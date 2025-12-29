from django.shortcuts import render
import shopify
import json
import shopify
from functools import wraps
from authentication.models import ShopifyStore
from pathlib import Path
from authentication.models import ShopifyStore



def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url') # Get shop url from the link
        
        if not shop_url: # No shop url entered -> Error page with error code A01
            BASE_DIR = Path(__file__).resolve().parent # Base directory 

            with open(f"{BASE_DIR.parent}/data/error_codes.json") as file: # Get error code from the json file 
                d = json.load(file)
            error_code = "A01"
            error_message = d["authentication_errors"][error_code]
            return render(request, 'error_page.html', {'error_code': error_code, 'error_message': error_message}) 
        
        try:
            shop_data = ShopifyStore.objects.get(shopify_domain=shop_url)
            # Create and activate the session
            session = shopify.Session(shop_data.shopify_domain, "2024-10", shop_data.access_token)
            shopify.ShopifyResource.activate_session(session)
        except ShopifyStore.DoesNotExist: # No valid shop url -> Error page with error code A02
            BASE_DIR = Path(__file__).resolve().parent
            with open(f"{BASE_DIR.parent}/data/error_codes.json") as file:
                d = json.load(file)
            error_code = "A02"
            error_message = d["authentication_errors"][error_code]
            return render(request, 'error_page.html', {'error_code': error_code, 'error_message': error_message}) 

        return f(request, *args, **kwargs) # Return regular request
    return decorated_function


@shopify_auth_required
def home(request):
    shop = shopify.Shop.current()
    shop_url = shop.myshopify_domain 
    current_plan = ShopifyStore.objects.get(shopify_domain=shop_url).plan_name
    # Information from the shopify server
    shop_name = shop.name          # Name of the shop
    # shop_owner = shop.shop_owner   
    # shop_email = shop.email
    products = shopify.Product.find()

    context = {
        'products': products,
        'shop_url': shop_url,
        'shop_name': shop_name,
        'user_plan': current_plan
    }
            

    return render(request, 'index.html', context)

@shopify_auth_required
def product_analysis(request):
    shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url')
    current_plan = ShopifyStore.objects.get(shopify_domain=shop_url).plan_name
    product_id = request.GET.get('product')
    product_id = product_id.replace('/','')
    product = shopify.Product.find(product_id)
    
    # Calculations for the dashboard
    total_inventory = sum(v.inventory_quantity for v in product.variants)
    price_min = min(float(v.price) for v in product.variants)
    price_max = max(float(v.price) for v in product.variants)
    
    context = {
        'product': product,
        'user_plan': current_plan,
        'total_inventory': total_inventory,
        'price_range': f"{price_min:.2f} - {price_max:.2f}" if price_min != price_max else f"{price_min:.2f}",
        'shop_name': shopify.Shop.current().name,
        'shop_url': shop_url
    }
    return render(request, 'product_analysis.html', context)

