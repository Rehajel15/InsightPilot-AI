# Create your views here.
import shopify
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import ShopifyStore
from django.contrib import messages

def shopify_login(request):
    shop_url = request.GET.get('shop')
    if not shop_url:
        return HttpResponse("Please enter a shop parameter", status=400)

    # Initialize the Shopify-Session
    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    
    permission_url = shopify.Session(shop_url, "2024-10").create_permission_url(
        settings.SHOPIFY_SCOPES, 
        f"{settings.SHOPIFY_APP_URL}/auth/callback"
    )
    return redirect(permission_url)



def shopify_callback(request):
    params = request.GET.dict()
    shop_url = params.get('shop')
    
    # Initialize the session to exchange the code for a token
    session = shopify.Session(shop_url, "2024-10")
    access_token = session.request_token(params)
    
    # Save or update the store credentials in our database
    store, created = ShopifyStore.objects.update_or_create(
        shopify_domain=shop_url,
        defaults={'access_token': access_token}
    )
    
    if created:
        messages.success(request, f"Successfully installed on {shop_url}!")
    else:
        messages.info(request, f"Settings updated for {shop_url}.")

    # Redirect to your dashboard or product list
    return redirect(f"/?shop={shop_url}")