from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'), # path to checkout section
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    # order number as an argument for each purchase
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    # to view cache checkout data
    path('wh/', webhook, name='webhook'), # a path for webhook_handler
]