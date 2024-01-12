from django import forms
from .models import Order

# check out form
class OrderForm(forms.ModelForm):
    """User field when checkout"""
    class Meta:
        model = Order
        # fields to be completed
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        to set up the init method, add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            # This placeholder are shown in the fields to complete by the user
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        # set autofocus field to true so the cursor starts in the full name when the user loads the page
        for field in self.fields:
            # I have an error with country since I installed django-countries so I have to deleted
            # from my placeholders and changed it here as well
            if field != 'country':
                # iterate through the form fields 
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                # if the field is required would be marked with a star
                else:
                    # otherwise setting all the placeholders to the values
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False