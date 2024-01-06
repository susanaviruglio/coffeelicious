from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def all_products(request):
    """A view to show all coffee products, including sorting and search queries by the user"""

    products = Product.objects.all() #to import the products model from the db
    query = None 
    # query is equal to none to avoid errors when loading the page
    categories = None
    # categories is equal to none to avoid errors when selecting them


    if request.GET:
        """to access product parameter in the search form I need to check if request exists,
        the text input in that form was named 'q'"""

        if 'category' in request.GET:
            # to access the product sorted by category selected
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            # looking for the name field of the category model
            categories = Category.objects.filter(name__in=categories)
            # filter all categories by its object name


        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You haven't entered any search criteria!")
                return redirect(reverse('products'))

            # Q generates a search query in order to filter a list of products
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # name and description contain the query and the i infront makes the queries insensitive
            products = products.filter(queries)
            # I passed the queries in order to filter the products


    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
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