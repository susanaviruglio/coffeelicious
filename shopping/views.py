from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.
def shopping_bag(request):
    """A view to return the shopping bag """
    
    return render(request, 'shopping/shopping.html')


def add_to_shopping_bag(request, item_id):
    """ to add times to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    # turn into an int so it the function does not return a string
    redirect_url = request.POST.get('redirect_url')
    # to redirect the user to the previous url when an item has been purchased

    bag = request.session.get('bag', {})
    # this variable allows items to be store while the user keeps shopping

    if item_id in list(bag.keys()):
       
        bag[item_id] += quantity
        # if there's already a product then increment the quantity
    else:
        bag[item_id] = quantity
        # item id is equal to the quantity

    request.session['bag'] = bag
    # add the session again with the updated item

    return redirect(redirect_url)


def adjust_shopping_bag(request, item_id):
    """ update the shopping bag and ensure the specific amount"""

    quantity = int(request.POST.get('quantity'))
    # turn into an int so it the function does not return a string

    bag = request.session.get('bag', {})
    # this variable allows items to be store while the user keeps shopping


    if quantity > 0:
        # if the quantity is bigger than 0 then the item is equal to the current quantity
        bag[item_id] = quantity
    else:
        bag.pop(item_id)
        # otherwise delete item if is less than 0 


    request.session['bag'] = bag
    # add the session again with the updated item

    return redirect(reverse('shopping_bag'))



def delete_item_bag(request, item_id):
    """ Remove items from the shopping bag """

    try:
        bag = request.session.get('bag', {})
        if item_id in bag:
            bag.pop(item_id)
            request.session['bag'] = bag
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    except Exception as e:
        return HttpResponse(status=500)