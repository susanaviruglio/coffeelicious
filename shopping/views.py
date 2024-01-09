from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.
def shopping_bag(request):
    """A view to return the shopping bag """
    
    return render(request, 'shopping/shopping.html')


def add_to_shopping_bag(request, item_id):
    """ to add times to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    # to get the product to send messages to users with the primary key
    # added get object or 404 in case the item does not exist or it is not there

    quantity = int(request.POST.get('quantity'))
    # turn into an int so it the function does not return a string
    redirect_url = request.POST.get('redirect_url')
    # to redirect the user to the previous url when an item has been purchased

    bag = request.session.get('bag', {})
    # this variable allows items to be store while the user keeps shopping

    if item_id in list(bag.keys()):
       
        bag[item_id] += quantity
        # if there's already a product then increment the quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}.')

    else:
        bag[item_id] = quantity
        # item id is equal to the quantity
        messages.success(request, f'Added {product.name} to your shopping bag.')
        # add message when a product has been added to the bag

    request.session['bag'] = bag
    # add the session again with the updated item
    
    

    return redirect(redirect_url)


def adjust_shopping_bag(request, item_id):
    """ update the shopping bag and ensure the specific amount"""

    product = get_object_or_404(Product, pk=item_id)
    # to get the product to send messages to users with the primary key
    # added get object or 404 in case the item does not exist or it is not there

    quantity = int(request.POST.get('quantity'))
    # turn into an int so it the function does not return a string

    bag = request.session.get('bag', {})
    # this variable allows items to be store while the user keeps shopping


    if quantity > 0:
        # if the quantity is bigger than 0 then the item is equal to the current quantity
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}.')
        # message to update
    else:
        bag.pop(item_id)
        # otherwise delete item if is less than 0
        messages.success(request, f'Removed {product.name} from your shopping bag.')


    request.session['bag'] = bag
    # add the session again with the updated item

    return redirect(reverse('shopping_bag'))



def delete_item_bag(request, item_id):
    """ Remove items from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        # to get the product to send messages to users with the primary key
        # added get object or 404 in case the item does not exist or it is not there
        bag = request.session.get('bag', {})
        # when request session to get bag
        if item_id in bag:
            # if the item is in the bag then delete it
            bag.pop(item_id)
            request.session['bag'] = bag
            messages.success(request, f'Removed {product.name} from your shopping bag.')

            return HttpResponse(status=204)
            
        else:
            return HttpResponse(status=404)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        # the user will get a message error rather than view error
        return HttpResponse(status=500)