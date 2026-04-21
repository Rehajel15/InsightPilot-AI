# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create new migration after model changes
python manage.py makemigrations

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test authentication
python manage.py test core
python manage.py test billing

# Open Django shell
python manage.py shell
```

## Architecture

**InsightPilot AI** is a Django-based Shopify embedded app that provides AI-powered product analytics for Shopify merchants. It authenticates via Shopify OAuth and displays product data within the Shopify admin iframe.

### Apps

| App | Responsibility |
|-----|---------------|
| `authentication` | Shopify OAuth flow, `ShopifyStore` model (domain, access token, plan) |
| `billing` | Subscription pricing page, Shopify recurring charges, webhook handling |
| `core` | Product dashboard (index), product analysis page, error page |

### URL Structure

```
/           → core.urls   (home, product_analysis)
/auth/      → authentication.urls  (login, callback)
/billing/   → billing.urls  (pricing, subscribe, activate, webhooks)
/admin/     → Django admin
```

### Authentication Pattern

All protected views use the `@shopify_auth_required` decorator defined in `core/views.py`. It reads the `shop` query parameter, validates the domain, looks up the `ShopifyStore`, and activates a Shopify API session. On failure, it renders `error_page.html` with a code looked up from `data/error_codes.json`.

### Plan-Gated Features

`ShopifyStore.plan_name` has three values: `Free`, `Basic`, `Premium`. Templates check the plan to show/hide AI analysis boxes — see `product_analysis.html` for the conditional rendering pattern.

### Shopify Embedded App Settings

Several settings in `settings.py` are required for Shopify iframe embedding and must not be changed without understanding the implications:
- `SESSION_COOKIE_SAMESITE = 'None'` / `SESSION_COOKIE_SECURE = True`
- `CSRF_TRUSTED_ORIGINS` includes `*.myshopify.com` and `*.shopify.com`
- `X_FRAME_OPTIONS = 'ALLOWALL'`
- `CSP_FRAME_ANCESTORS` whitelist for Shopify domains
- `NgrokSkipWarningMiddleware` in `InsightPilot_AI/middleware.py` adds the ngrok bypass header for local development via ngrok tunnel.

### Billing / Webhook Flow

`billing/signals.py` registers a `post_save` signal on `ShopifyStore`. When a new store is created, it automatically registers a Shopify webhook for `app_subscriptions_update` pointing to `/billing/webhooks/subscription-update/`. The billing views use `RecurringApplicationCharge` from the ShopifyAPI to create and activate subscriptions.

### Environment Variables

All secrets are in `.env` (not committed). Required keys:
```
SECRET_KEY, DEBUG, ALLOWED_HOSTS, APP_DOMAIN,
SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_APP_URL, SHOPIFY_SCOPES
```

### Frontend

- Bootstrap 5 (local static files in `/static/`)
- Django templates with `APP_DIRS=True` (each app has its own `templates/` folder)
- `static/js/searchField.js` — real-time product search filter on the dashboard

### Key Dependencies

- `Django==6.0`
- `ShopifyAPI==12.7.0` — wraps Shopify REST API via ActiveResource
- `python-dotenv==1.2.1` — loads `.env`
- `PyJWT==2.10.1` — JWT handling for Shopify session tokens
