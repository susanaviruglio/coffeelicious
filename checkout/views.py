from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from shopping.contexts import shopping_contents
import stripe


# View of the checkout shopping bag
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # variables with the secret key and public key

    if request.method == 'POST':
        # to add the payment to the database by requesting method POST
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # if the form is valid then save the order
            order = order_form.save()
            for item_id, item_data in bag.items():
                # iterate through the items 
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                        )
                    order.delete()
                    return redirect(reverse('shopping_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            # if the user want to save the information to their profile or not
            return redirect(reverse('checkout_success', args=[order.order_number]))
            # redirect the user to checkout success with order number as an argument
        else:
            # if the order form is not valid then load this message at the bottom of the page
            messages.error(request, 'There was an error with your form. \
                    Please double check your information.')
    else:
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


def checkout_success(request, order_number):
    """
    To let users know that their payment was succesfully completed
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        # delete the shopping bag when the session is finished
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)