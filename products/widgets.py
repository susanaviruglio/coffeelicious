from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


# to improve css in the image when editing or adding products
class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'