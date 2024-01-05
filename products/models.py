from django.db import models

# Create your models here.
class Category(models.Model):
    """Fixtures goes into this model, I have created Categories names to organize 
    each product in different sections"""

    class Meta:
        """meta class added to correct spelling mistake in django befores was categorys"""
        verbose_name_plural = 'Categories'

    # character field which represents the product
    name = models.CharField(max_length=254) 
    
    # friendly name for the user to identify each category
    friendly_name = models.CharField(max_length=254, null=True, blank=True) 

    def __str__(self):
        """a string method that takes the category model itself"""
        return self.name

    def get_friendly_name(self):
        """a string method that returns the friendly name itself"""
        return self.friendly_name


class Product(models.Model):
    """ A table for each product: the first field is a foreign key to the category model,
    then sku is a specific identification number, product name, product description, etc.
    Each product requires a name, a description and a price ,but the rest it is optional."""

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        """the string method returns the product's name itself"""
        return self.name