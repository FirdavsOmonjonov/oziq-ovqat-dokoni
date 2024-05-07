from django.urls import path
from .views import ProductList, AllProductsList, SortingProductsList, SortingBySubcategories,ProductDetail,sorting_by_subcategories, rate


urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductsList.as_view(), name='all_products'),
    path('sorting/<slug:key_name>/', SortingProductsList.as_view(), name='sorting'),
    path('subcategory/<slug:slug>/', SortingBySubcategories.as_view(), name='subcategory'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('subcategory/<slug:slug>/',sorting_by_subcategories, name='subcategory'),
    path('rate/<int:product_id>/<int:rating>/', rate)
]