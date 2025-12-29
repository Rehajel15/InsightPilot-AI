import json
import shopify
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from authentication.models import ShopifyStore
from views import shopify_auth_required

# 1. Show the pricing plans
def pricing_page(request):
    return render(request, 'pricing.html')

# 2. Create the charge and redirect to Shopify
@shopify_auth_required
def create_subscription(request, plan_type):
    # Mapping the plan types to names and prices
    plans = {
        'basic': {'name': 'Basic Plan', 'price': 14.99},
        'premium': {'name': 'Premium Plan', 'price': 29.99}
    }
    
    selected_plan = plans.get(plan_type)
    if not selected_plan:
        return redirect('pricing')

    # Create a Recurring Charge in Shopify
    charge = shopify.RecurringApplicationCharge.create({
        "name": selected_plan['name'],
        "price": selected_plan['price'],
        "return_url": f"https://{settings.APP_DOMAIN}/billing/charge-callback/",
        "test": True, # SET TO FALSE FOR LIVE APPS
        "trial_days": 7
    })

    # Send user to Shopify's approve page
    return redirect(charge.confirmation_url)

# 3. Activate the charge after user clicked 'Approve'
@shopify_auth_required
def activate_subscription(request):
    charge_id = request.GET.get('charge_id')
    if not charge_id:
        return redirect('pricing')

    # Find and activate the charge
    charge = shopify.RecurringApplicationCharge.find(charge_id)
    if charge.status == "accepted":
        charge.activate()
    
    return redirect('dashboard') # Or wherever your home view is

# 4. The Webhook receiver (The silent listener)
@csrf_exempt
def webhook_subscription_update(request):
    # Shopify sends data as a POST request
    try:
        data = json.loads(request.body)
        shop_domain = request.headers.get('X-Shopify-Shop-Domain')
        
        subscription = data.get('app_subscription', {})
        status = subscription.get('status') # e.g., 'ACTIVE', 'CANCELLED'
        plan_name = subscription.get('name')

        # Update the database
        shop = ShopifyStore.objects.get(shopify_domain=shop_domain)
        
        if status == 'ACTIVE':
            shop.plan_name = plan_name
        else:
            shop.plan_name = 'Free' # Fallback for cancelled/frozen
            
        shop.save()
        return HttpResponse(status=200)
        
    except Exception as e:
        print(f"Webhook Error: {e}")
        return HttpResponseBadRequest()