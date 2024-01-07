from decimal import Decimal
from django.conf import settings

def shopping_contents(request):

    purchase_items = [] # items purchase in the bag
    total = 0 # start counting from 0
    purchase_count = 0 # start purchasing from 0

    # if the user buys certain amount of items then the delivery would be
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # if the total is less than the certain amout it would multiply total times standar percentage
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        # to know how much need to spend left to get free delivery, certain amout take away total
    else:
        delivery = 0
        # otherwise if the amout is greater or the same
        free_delivery_delta = 0
        # then free delivery so it is equal to 0
    
    purchase_total = delivery + total
    # to calculate all the amout will be delivery add the total

    context = {
        'purchase_items': purchase_items,
        'total': total,
        'purchase_count': purchase_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'purchase_total': purchase_total
    }

    return context