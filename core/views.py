from django.shortcuts import render
from django.core.cache import cache
import shopify
import json
from functools import wraps
from authentication.models import ShopifyStore
from pathlib import Path

CACHE_TTL = 300  # 5 minutes

_BASE_DIR = Path(__file__).resolve().parent.parent
with open(_BASE_DIR / 'data' / 'error_codes.json') as _f:
    _ERROR_CODES = json.load(_f)


def _render_error(request, code):
    return render(request, 'error_page.html', {
        'error_code': code,
        'error_message': _ERROR_CODES["authentication_errors"][code],
    })


def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url')

        if not shop_url:
            return _render_error(request, "A01")

        try:
            shop_data = ShopifyStore.objects.get(shopify_domain=shop_url)
            session = shopify.Session(shop_data.shopify_domain, "2024-10", shop_data.access_token)
            shopify.ShopifyResource.activate_session(session)
        except ShopifyStore.DoesNotExist:
            return _render_error(request, "A02")

        try:
            return f(request, *args, **kwargs)
        finally:
            shopify.ShopifyResource.clear_session()

    return decorated_function


@shopify_auth_required
def home(request):
    shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url')

    shop_cache_key = f'shop_data_{shop_url}'
    shop = cache.get(shop_cache_key)
    if shop is None:
        shop = shopify.Shop.current()
        cache.set(shop_cache_key, shop, CACHE_TTL)

    current_plan = ShopifyStore.objects.get(shopify_domain=shop.myshopify_domain).plan_name

    products_cache_key = f'products_{shop_url}'
    products = cache.get(products_cache_key)
    if products is None:
        products = shopify.Product.find(limit=250)
        cache.set(products_cache_key, products, CACHE_TTL)

    context = {
        'products': products,
        'shop_url': shop.myshopify_domain,
        'shop_name': shop.name,
        'user_plan': current_plan
    }

    return render(request, 'index.html', context)

@shopify_auth_required
def product_analysis(request):
    shop_url = request.GET.get('shop') or request.session.get('shopify_shop_url')
    current_plan = ShopifyStore.objects.get(shopify_domain=shop_url).plan_name
    product_id = request.GET.get('product')
    product_id = product_id.replace('/', '')

    product_cache_key = f'product_{shop_url}_{product_id}'
    product = cache.get(product_cache_key)
    if product is None:
        product = shopify.Product.find(product_id)
        cache.set(product_cache_key, product, CACHE_TTL)

    shop_cache_key = f'shop_data_{shop_url}'
    shop = cache.get(shop_cache_key)
    if shop is None:
        shop = shopify.Shop.current()
        cache.set(shop_cache_key, shop, CACHE_TTL)

    total_inventory = sum(v.inventory_quantity for v in product.variants)
    price_min = min(float(v.price) for v in product.variants)
    price_max = max(float(v.price) for v in product.variants)

    tags = [t.strip() for t in product.tags.split(',') if t.strip()]

    context = {
        'product': product,
        'user_plan': current_plan,
        'total_inventory': total_inventory,
        'price_range': f"{price_min:.2f} - {price_max:.2f}" if price_min != price_max else f"{price_min:.2f}",
        'shop_name': shop.name,
        'shop_url': shop_url,
        'tags': tags,
    }
    return render(request, 'product_analysis.html', context)

