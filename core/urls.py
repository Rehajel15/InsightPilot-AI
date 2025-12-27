from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('analysis/', views.product_analysis, name='product_analysis')
]
