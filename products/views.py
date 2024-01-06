from django.shortcuts import render, get_object_or_404
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



def product_description(request, product_id):
    """A view to show individual product with their personal description"""

    product = get_object_or_404(Product, pk=product_id)


    context = {
        'product': product
    }


    # it need to return a context so I have to send information back to the template
    return render(request, 'products/product_description.html', context)