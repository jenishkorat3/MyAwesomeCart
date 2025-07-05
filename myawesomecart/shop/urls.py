from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="ShopAbout"),
    path('contact/', views.contact, name="ShopContact"),
    path('products/<int:id>/', views.productDetail, name="ProductDetail"),
    path('checkout/', views.checkout, name="ShopCheckout"),
    path('tracker/', views.tracker, name="ShopTracker"),
]
