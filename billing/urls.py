from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.pricing_page, name='pricing'),
    path('subscribe/<str:plan_type>/', views.create_subscription, name='create_sub'),
    path('charge-callback/', views.activate_subscription, name='charge_callback'),
    path('webhooks/subscription-update/', views.webhook_subscription_update, name='sub_webhook'),
]