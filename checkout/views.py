from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from shopping.contexts import shopping_contents
import stripe
import json # to access the metadata


@require_POST
def cache_checkout_data(request):
    """give the client secret for the payment intent"""
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        # payment Id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # to modify the payment intent
        stripe.PaymentIntent.modify(pid, metadata={
            # to modify I need the information
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            # added stripe 
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag) 
            order.save()
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


        if request.user.is_authenticated:
            # if the user is authenticated
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()
            # instance of the order form

  

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

    if request.user.is_authenticated:
        """Add a user profile when the checkout is succesful
        if the request user is authenticated"""

        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            """If the payment is checked then added to the users' profile"""
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                # if the user form is valid then save it
                user_profile_form.save()

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