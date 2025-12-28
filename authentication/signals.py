# signals.py
import shopify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ShopifyStore

@receiver(post_save, sender=ShopifyStore)
def register_webhooks_on_install(sender, instance, created, **kwargs):
    """
    Automatically register the subscription webhook when a new shop is created.
    """
    if created:
        try:
            # 1. Start a Shopify Session
            session = shopify.Session(instance.shopify_domain, "2024-01", instance.access_token)
            shopify.ShopifyResource.activate_session(session)

            # 2. Define the Webhook
            webhook = shopify.Webhook()
            webhook.topic = "app_subscriptions_update"
            # Replace with your actual live URL or ngrok URL for testing
            webhook.address = f"https://{settings.APP_DOMAIN}/webhooks/subscription-update/"
            webhook.format = "json"

            # 3. Save the Webhook to Shopify
            if webhook.save():
                print(f"Success: Webhook registered for {instance.shopify_domain}")
            else:
                print(f"Error: {webhook.errors.full_messages()}")
        
        except Exception as e:
            print(f"Critical Error during Webhook registration: {str(e)}")
        
        finally:
            # Always clear the session to avoid leaks
            shopify.ShopifyResource.clear_session()