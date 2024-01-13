from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

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