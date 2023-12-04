from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from .models import Product, Category, UserSavedProduct
from .forms import ProductForm
import random
# Create your views here.


def all_products(request):
    """ All products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    all_categories = Category.objects.exclude(name='all_products')
    random_category = random.choice(all_categories)

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET.get('sort')
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter a search criteria!')
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'random_category': random_category,
        'all_categories': all_categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    # Fetch the list of all products
    all_products_list = Product.objects.all()
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'products': all_products_list,  # Pass the list of all products to the template
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    """ Delete a product in the store """
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted!')
        return HttpResponseRedirect(reverse('products'))

    context = {'product': product}
    return render(request, 'delete_product.html', context)


@login_required
def add_to_saved(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product is already saved for the current user
    saved_product, created = UserSavedProduct.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, 'Product saved for later!')
    else:
        saved_product.delete()
        messages.success(request, 'Product removed from saved!')

    return redirect('product_detail', product_id=product_id)

@login_required
def saved_for_later(request):
    saved_products = UserSavedProduct.objects.filter(user=request.user)
    return render(request, 'products/saved_for_later.html', {'saved_products': saved_products})
