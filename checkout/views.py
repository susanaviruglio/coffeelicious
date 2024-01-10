from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm 
from shopping.contexts import shopping_contents
import stripe

# View of the checkout shopping bag
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # variables with the secret key and public key

    bag = request.session.get('bag', {})
    # to access the items from the shopping bag
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        # if the shopping bag is empty this message will appear
        return redirect(reverse('products'))
        # to prevent people to type /checkout in the url

    current_bag = shopping_contents(request)
    total = current_bag['purchase_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        # create the payment intent with the amount and the currency
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm() # instance of the order form
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    # template html
    context = {
        'order_form': order_form, 
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
    