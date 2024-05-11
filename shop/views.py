from django.views.generic import ListView, DetailView
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Category, Product, Rating
from django.shortcuts import render, redirect
from shop import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            return render(request,'auth/error.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def log_in(request):
    """Log in to"""
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request,'auth/error.html')
        except:
            return redirect('index')
    return render(request, 'auth/login.html')


def log_out(request):
    """Log out of"""
    logout(request)
    return redirect('error2')


def error1(request):
    """Login error"""
    return render(request, 'auth/error.html')

def error2(request):
    """Admin panel error"""
    return render(request, 'auth/error2.html')




"""Class yordamida yozilgan view"""
# @login_required(login_url='login')
class ProductList(ListView, LoginRequiredMixin):
    """Product list view at class level."""
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'title': "Fruitables online shop",
        'page_name': "Shop",
    }

    

class AllProductsList(ProductList):
    """All products list view at class level"""
    template_name = 'shop/all_products.html'


class SortingProductsList(AllProductsList):
    """Sorting products list view at class level"""
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(filter_choice=self.kwargs['key_name'])
        context['products'] = products
        return context


class SortingBySubcategories(AllProductsList):
    """Sorting by subcategories list view at class level"""
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = subcategory.product_set.all()
        return context


class ProductDetail(DetailView, LoginRequiredMixin):
    """Product detail view at class level"""
    model = Product
    template_name ='shop/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object  # Access the current product instance
        rating = Rating.objects.filter(product=product, user=self.request.user).first()
        context['user_rating'] = rating.rating if rating else 0
        related_products = Product.objects.filter(category=self.object.category)
        context['page_name'] = "Shop Details"
        context['categories'] = Category.objects.filter(parent=None)
        context['products'] = related_products
        return context


"""Funkisi yordamida yozilgan view"""
@login_required(login_url='login')
def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', id = product.id)


@login_required(login_url='login')
def sorting_by_subcategories(request, slug):
    """Sorting by subcategories view at func level"""
    subcategory = Category.objects.get(slug=slug)
    context={
        'categories':Category.objects.filter(parent=None),
        'products': subcategory.product_set.all(),
    }
    return render(request, 'shop/detail.html', context)


@login_required(login_url='login')
def detail(request , product_id):
    """Product detail view at func level"""
    product = Product.objects.get(id=product_id)
    products = Product.objects.filter(category=product.category)
    context = {
        'product': product,
        'categories': Category.objects.filter(parent=None),
        'page_name': "Shop Detail",
        'products': products
    }
    return render(request,'shop/detail.html', context)


@login_required(login_url='login')
def sorting(request: HttpRequest, key_name) -> HttpResponse:
    """Sorting products view at func level"""
    context = {
        'products': Product.objects.filter(filter_choice=key_name),
        'categories': Category.objects.filter(parent=None)
        
    }
    return render(request, 'shop/all_products.html', context)
