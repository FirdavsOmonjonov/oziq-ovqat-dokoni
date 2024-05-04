from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'quantity', 'category', 'get_image')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px;">')
        return '-'

    get_image.short_description = 'Rasmi'

    prepopulated_fields = {'slug': ('name',)}


