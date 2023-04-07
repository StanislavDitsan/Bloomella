from django.shortcuts import render

# Create your views here.


def all_products(request):
    """ All products, including sorting and search queries """

    products = Products.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
