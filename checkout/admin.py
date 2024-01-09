from django.contrib import admin
from .models import Order, OrderLineItem # modules added 


class OrderLineItemAdminInline(admin.TabularInline):
    """Allow adming to edit in line the items"""

    model = OrderLineItem
    # allow to edit items right inside the order module
    readonly_fields = ('lineitem_total',) # to view a list of items 


class OrderAdmin(admin.ModelAdmin):
    """Items purchased details display in the admin area"""
    
    inlines = (OrderLineItemAdminInline,) 

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'purchase_total',) # read only fields

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'purchase_total',) # personal fields

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'purchase_total',) # display product list

    ordering = ('-date',) # order date

admin.site.register(Order, OrderAdmin) # admin register to the site