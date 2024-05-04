from django.urls import path
from .views import ProductList, AllProductsList, SortingProductsList, SortingBySubcategories, detail,sorting_by_subcategories


urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductsList.as_view(), name='all_products'),
    path('sorting/<slug:key_name>/', SortingProductsList.as_view(), name='sorting'),
    path('subcategory/<slug:slug>/', SortingBySubcategories.as_view(), name='subcategory'),
    path('detail/<int:product_id>/', detail, name='detail'),
    path('subcategory/<slug:slug>/',sorting_by_subcategories, name='subcategory'),
]