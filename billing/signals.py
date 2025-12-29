import shopify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from authentication.models import ShopifyStore 

@receiver(post_save, sender=ShopifyStore)
def register_webhooks_on_install(sender, instance, created, **kwargs):
    """
    When a new shop is saved (installation), register the subscription webhook.
    """
    if created:
        try:
            # Create a session for the shop
            session = shopify.Session(instance.shopify_domain, "2024-01", instance.access_token)
            shopify.ShopifyResource.activate_session(session)

            # Register the App Subscription Update Webhook
            webhook = shopify.Webhook()
            webhook.topic = "app_subscriptions_update"
            # The URL points to the webhook view in this app
            webhook.address = f"https://{settings.APP_DOMAIN}/billing/subscription-update/"
            webhook.format = "json"

            if webhook.save():
                print(f"Webhook registered for {instance.shopify_domain}")
            else:
                print(f"Webhook failed: {webhook.errors.full_messages()}")
        
        except Exception as e:
            print(f"Error registering webhook: {e}")
        finally:
            shopify.ShopifyResource.clear_session()