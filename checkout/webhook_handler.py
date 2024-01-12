from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time # imported time module from Python


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        # the init method is called everytime an instance of a class is created
        self.request = request

    def handle_event(self, event):
        """
        It take the event that it has been sent and return a HTTP response
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe everytime a user
        completes a payment
        """
        intent = event.data.object
        # if the user closes the page 
        pin = intent.id 
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details # updated
        shipping_details = intent.shipping
        purchase_total = round(stripe_charge.amount / 100, 2) # updated

         # Clean data in the shipping details for the database
        for field, value in shipping_details.address.items():
            if value == "":
                # stripe will store it as an empty string as none otherwise would be null
                shipping_details.address[field] = None

        order_exists = False # if the order does not exist would be created in the webhook
        attempt = 1 # delay in case the web goes slow
        while attempt <= 5:
            try: # a while loop that executes up to 5 times before creating the order itself
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    purchase_total=purchase_total,
                    original_bag=bag,
                    stripe_pid=pid,
                    )
                order_exists = True 
                break # break the loop if the order is found

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200) # order exists load this message
        else:
            order = None
            try: # otherwise it will create the order
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                            )
                            order_line_item.save()

            except Exception as e:
                if order:
                    order.delete() #if something goes wrong the order will be deleted
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500) # then return a 500 Error to Strike
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)