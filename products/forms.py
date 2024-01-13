from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category

# allow superuser the ability to add and delete forms
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product 
        fields = '__all__' # select all the fields

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names # view of the friendly names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'