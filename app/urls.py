from django.urls import path
from .views import publish_order_to_buy, publish_order_to_sell

urlpatterns = [
    path('publish_order_to_buy/',publish_order_to_buy , name='publish_order_to_buy'),
    path('publish_order_to_sell/', publish_order_to_sell, name='publish_order_to_sell'),
]