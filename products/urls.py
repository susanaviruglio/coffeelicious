from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'), # path for all the products
    path('<int:product_id>/', views.product_description, name='product_description'), 
    # product description file path, it should be an integer
    path('add/', views.add_product, name='add_product'), # path for adding more products to the store
]