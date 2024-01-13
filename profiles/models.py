from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save # ensure that signal worsk
from django.dispatch import receiver

from django_countries.fields import CountryField

# User profile model that creates automatically a profile for each user who sings up.
class UserProfile(models.Model):
    """
    User profile model that has one to one field attached to the user.
    The rest of the fields are delivery information and all of them are optional.
    """
    #each user is allowed to have only one profile and each profile only can be attached to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        # string method which returns the user name
        return self.user.username


@receiver(post_save, sender=User) # receiver event from the user model
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile 
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()

