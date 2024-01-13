from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
# a view of the profile 
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    # if there is any error then show error 404

    if request.method == 'POST':
        # if the request is POST then instance profile is applied
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # if the is valid then it will be saved and it will show a message
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            # other wise it would show that it failed.
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
        # to get user profile form
    orders = profile.orders.all()
    # to get the users orders

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)



def order_history(request, order_number):
    """Order History view for My Profile, very similar to the function on the top"""

    order = get_object_or_404(Order, order_number=order_number)
    # if there is any error then show error 404

    messages.info(request, (
        f'This is a message for the past order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    # template and context which includes an order number

    context = {
        'order': order,
        'from_profile': True, # to check if the user gets on the template the order view
    }

    return render(request, template, context)