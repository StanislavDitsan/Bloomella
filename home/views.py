from django.shortcuts import render
from testimonials.models import Testimonial
from products.models import Product, Category


def index(request):
    """ A view to return the index page and the testimonials """
    testimonials = Testimonial.objects.filter(approved=True)

    products = Product.objects.all()[:4]
    all_categories = Category.objects.exclude(name='all_products')

    context = {
        'testimonials': testimonials,
        'products': products,
        'all_categories': all_categories,
    }
    return render(request, 'home/index.html', context)
