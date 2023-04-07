from django.contrib import admin
from .models import Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'in_stock',
        'image',
    )

    ordering = ('sku', )

    search_fields = ('name', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

    search_fields = ('name', )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
