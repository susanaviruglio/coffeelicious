from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm #

# View of the checkout shopping bag
def checkout(request):
    bag = request.session.get('bag', {})
    # to access the items from the shopping bag
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        # if the shopping bag is empty this message will appear
        return redirect(reverse('products'))
        # to prevent people to type /checkout in the url

    order_form = OrderForm() # instance of the order form
    template = 'checkout/checkout.html'
    # template html
    context = {
        'order_form': order_form, 
        'stripe_public_key': 'pk_test_51OWoCBLhM6oOpGXPJmNXodBnu3fsZ3RDM2paOQHtnAf8dipMh0HV8bMnKiQ1iy5oBsN2WNV6mhMsszGzwKhlxswQ00YJTTyie9',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
    