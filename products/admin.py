from django.contrib import admin
from .models import Product, Category

# I have registered Product and Category to be able to see it 
admin.site.register(Product)
admin.site.register(Category)