from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    """A view to show all coffee products, including sorting and search queries by the user"""

    products = Product.objects.all() #to import the products model from the db


    context = {
        'products': products
    }


    # it need to return a context so I have to send information back to the template
    return render(request, 'products/products.html', context)