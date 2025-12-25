from django.db import models

class ShopifyStore(models.Model):
    # Store the unique .myshopify.com domain
    shopify_domain = models.CharField(max_length=255, unique=True)
    # The master key for API access
    access_token = models.CharField(max_length=255)
    
    # Timestamps for better tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.myshopify_domain