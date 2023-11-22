from django.urls import path 

from . import views 

urlpatterns = [
    path('',views.products, name = "product_home"),
    path('product_checkout/',views.product_checkout, name = "product_checkout"),
    path('product_cart/',views.product_cart, name = "product_cart"),

    path('update_item/',views.updateItem, name = "update_item"),
]