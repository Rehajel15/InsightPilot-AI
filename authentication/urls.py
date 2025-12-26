from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopify_login, name='shopify_login'), # authentication page
    path('callback/', views.shopify_callback, name='shopify_callback'), # callback to get access token and save the shop in the db
]