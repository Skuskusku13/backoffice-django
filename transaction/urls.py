from django.urls import path

from transaction.views import TransactionsListView, OneTransactionView, RevenueByFilters

urlpatterns = [
    path('', TransactionsListView.as_view(), name='transactions_list'),
    path('<int:id>', OneTransactionView.as_view(), name='one_transaction'),
    path('CA/', RevenueByFilters.as_view(), name='revenue_by_filters')
]
