import uuid # to generate the order number
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product # order line items has a foreign key
from django_countries.fields import CountryField # to find countries 
from profiles.models import UserProfile # attached user profile to checkout model

class Order(models.Model):
    """ required data to order products"""
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # it must be unique so user are able to find previous purchases
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='orders')
    # user profile foreign key to the order to create the connection between user and checkout
    # it sets to NULL if the profile is deleted to allow to keep order history
    # black set to true for users who does not have an account 
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    purchase_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='') #original shopping bag created
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='') #stripe payment id

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # use the sum funtion accross the line item fields and 0 to prevent error if I delete all the items manually
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            # with the total amount is less than delivery free
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            # applied the cost of the delivery free
        else:
            self.delivery_cost = 0
            # otherwise delivery is equal to 0
        self.purchase_total = self.order_total + self.delivery_cost
        # then purchase total is equal to the sum of the shopping bag cost and the delivery cost
        self.save()
        # save it

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            # if it does not have a order number then generate one
            self.order_number = self._generate_order_number()
            # order number is equal to the equivalent generated order number
        super().save(*args, **kwargs)

    def __str__(self):
        # return the order number of the product 
        return self.order_number


class OrderLineItem(models.Model):
    """individual shopping bag item attached to the order"""
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    # foreign key related to the order
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    # foreign key related to product of the order
    quantity = models.IntegerField(null=False, blank=False, default=0)
    # required 
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    # required

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        # to know the total we need to multiply the product price times the quantity
        super().save(*args, **kwargs)

    def __str__(self):
        # return string with the sku number on the order number to identify it
        return f'SKU {self.product.sku} on order {self.order.order_number}'
