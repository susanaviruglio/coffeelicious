from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm 

# Create your views here.
def all_products(request):
    """A view to show all coffee products, including sorting and search queries by the user"""

    products = Product.objects.all() #to import the products model from the db
    query = None 
    # query is equal to none to avoid errors when loading the page
    categories = None
    # categories is equal to none to avoid errors when selecting them
    sort = None
    # to make sure that sort is defined and avoid errors
    direction = None
    # direction defined to avoid errors

    if request.GET:
        """to access product parameter in the search form I need to check if request exists,
        the text input in that form was named 'q'"""

        if 'sort' in request.GET:
            # to check if sort is in request method
            sortkey = request.GET['sort']
            sort = sortkey

            # if sort exists then it will be sort by key which in this case is by name
            if sortkey == 'name':
                # allows to add a temporary field no a model
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
                # it annotates the current list of products with a new field


            if sortkey == 'category':
                # to sort product by name instead of id
                sortkey = 'category__name'


            if 'direction' in request.GET:
                # if sort is there then I need to check in which direction ascending or descending
                direction = request.GET['direction']
                if direction == 'desc':
                    # to check if the direction is descending 
                    sortkey = f'-{sortkey}'
                    # reverse sortkey direction
            products = products.order_by(sortkey)
            # sort all the products out by using order_by method


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

    sorting_all = f'{sort}_{direction}'
    # return sorting method to the template

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'sorting_all': sorting_all,
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


# Django firsts check whether the user log in before executing the view
@login_required
# View for store owners to add products to the coffee store
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        # if the user is not a superuser
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home')) # redirected back to the home page


    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # get file 
        if form.is_valid():
            # if the form is valid then show a success message
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_description', args=[product.id]))
        else:
            # otherwise it would show that it has failed.
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
# to be able to edit the products in the store
def edit_product(request, product_id):
    """ Edit a product in the store """


    if not request.user.is_superuser:
        # if the user is not a superuser
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home')) # redirected back to the home page


    product = get_object_or_404(Product, pk=product_id)
    # if there is any error then show error
    if request.method == 'POST':
        # if the request is post then get the files 
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # if the form is valid then save and show a message
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_description', args=[product.id]))
        else:
            # otherwise it will add a fail statement
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        # message info to edit a product
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    # template directory
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_superuser:
        # if the user is not a superuser
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home')) # redirected back to the home page


    product = get_object_or_404(Product, pk=product_id)
    # in case there is any error
    product.delete()
    # delete product 
    messages.success(request, 'Product deleted successfully!')
    # message to show 
    return redirect(reverse('products'))