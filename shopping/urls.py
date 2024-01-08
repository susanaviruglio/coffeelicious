from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_bag, name='shopping_bag'), # path to shopping bag 
    path('add/<item_id>/', views.add_to_shopping_bag, name='add_to_shopping_bag'),# path to add items
    path('adjust/<item_id>/', views.adjust_shopping_bag, name='adjust_shopping_bag'), # update shopping bag
    path('remove/<item_id>/', views.delete_item_bag, name='delete_item_bag'), # update shopping bag
]

