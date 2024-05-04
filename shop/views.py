from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Category, Product


# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'title': "Fruitables online shop",
        'page_name': "Shop",
    }


class AllProductsList(ProductList):
    template_name = 'shop/all_products.html'


class SortingProductsList(AllProductsList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(filter_choice=self.kwargs['key_name'])
        context['products'] = products
        return context


class SortingBySubcategories(AllProductsList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = subcategory.product_set.all()
        return context

def detail(request , product_id):
    product = Product.objects.get(id=product_id)
    # category = Category.objects.filter()
    products = Product.objects.filter(category=product.category)
    context = {
        'product': product,
        'categories': Category.objects.filter(parent=None),
        'page_name': "Shop Detail",
        'products': products
    }
    return render(request,'shop/detail.html', context)

def detail_filter(request):
    
    return render(request,'shop/detail.html', context)

# def sorting(request: HttpRequest, key_name) -> HttpResponse:
#     context = {
#         'products': Product.objects.filter(filter_choice=key_name),
#         'categories': Category.objects.filter(parent=None)
        
#     }
#     return render(request, 'shop/all_products.html', context)


def sorting_by_subcategories(request, slug):
    subcategory = Category.objects.get(slug=slug)
    context={
        'categories':Category.objects.filter(parent=None),
        'products': subcategory.product_set.all(),
    }
    return render(request, 'shop/detail.html', context)


# def index(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#         'categories': Category.objects.all()
#     }
#     return render(request, 'shop/index.html', context)

