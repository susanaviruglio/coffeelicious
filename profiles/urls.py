from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'), # a path to the profile
    path('order_history/<order_number>', views.order_history, name='order_history'),
    # order history path
]