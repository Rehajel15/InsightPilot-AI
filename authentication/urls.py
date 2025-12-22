from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopify_login, name='shopify_login'),
    path('callback/', views.shopify_callback, name='shopify_callback'),
]