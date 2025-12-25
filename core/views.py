from django.shortcuts import render
import shopify
import json
import shopify
from functools import wraps
from authentication.models import ShopifyStore
from pathlib import Path

def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url')
        
        if not shop_url:
            # If no shop is provided, we might need to redirect to a login page
            BASE_DIR = Path(__file__).resolve().parent

            with open(f"{BASE_DIR.parent}/data/error_codes.json") as file:
                d = json.load(file)
            error_code = "A01"
            error_message = d["authentication_errors"][error_code]
            return render(request, 'error_page.html', {'error_code': error_code, 'error_message': error_message}) 
        
        try:
            shop_data = ShopifyStore.objects.get(shopify_domain=shop_url)
            # Create and activate the session
            session = shopify.Session(shop_data.shopify_domain, "2024-10", shop_data.access_token)
            shopify.ShopifyResource.activate_session(session)
        except ShopifyStore.DoesNotExist:
            BASE_DIR = Path(__file__).resolve().parent
            with open(f"{BASE_DIR.parent}/data/error_codes.json") as file:
                d = json.load(file)
            error_code = "A02"
            error_message = d["authentication_errors"][error_code]
            return render(request, 'error_page.html', {'error_code': error_code, 'error_message': error_message}) 

        return f(request, *args, **kwargs)
    return decorated_function

@shopify_auth_required
def home(request):
    shop_url = request.GET.get('shop') or request.session.get('shop_url')
    shop = shopify.Shop.current() 
    # Information from the shopify server
    shop_name = shop.name          # Name of the shop
    # shop_owner = shop.shop_owner   
    # shop_email = shop.email        

    return render(request, 'index.html', {'shop_url': shop_url, 'shop_name': shop_name})
