from django.db.models.signals import post_save, post_delete # signals from Django
from django.dispatch import receiver # to receive Django signas

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
# execute this function everytime the post save signal is sent using the receiver decorator
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create.
    sender of the signals, instance of the module, a boolean to know if it is a good instance or not,
    and kwards (any key word argument).
    """
    instance.order.update_total() #specific item order update

@receiver(post_delete, sender=OrderLineItem)
# execute this function everytime the post delete signal is sent using the receiver decorator
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total() # for specific items order update