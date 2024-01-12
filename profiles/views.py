from django.shortcuts import render, get_object_or_404

from .models import UserProfile

# a view of the profile 
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    # if there is any error then show error 404
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
    }

    return render(request, template, context)