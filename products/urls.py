from django.urls import path
from .views import ProductListView, OneProductView, UpdateProductView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:tig_id>', OneProductView.as_view(), name='one_product'),
    path('<int:tig_id>/update', UpdateProductView.as_view(), name='put_one_product')
]
