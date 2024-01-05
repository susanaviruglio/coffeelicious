from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    """ This model it improves the products admin in Django to make easier to manage, 
    it is a list that communicates to the admin which field display."""

    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    
    # I sorted all the products by Sku and If I want to change it I just need to add a minus sign.
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    """This model it improves the Category admin in Django to make easier to manage,
    it is a list that communicates to the admin which field display."""

    list_display = (
        'friendly_name',
        'name',
    )


# I have registered Product and Category to be able to see it 
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)