from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
# to update the subtotal of the price and quantity
def calc_subtotal(price, quantity):
    return price * quantity