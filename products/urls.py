from django.urls import path
from . import views
from .views import delete_product

urlpatterns = [
    path('', views.all_products, name="products"),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/',
         delete_product,
         name='delete_product'),
]
