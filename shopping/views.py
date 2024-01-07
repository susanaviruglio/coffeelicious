from django.shortcuts import render, redirect

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