from django.urls import path

from transaction.views import TransactionsListView, OneTransactionView, RevenuesAndBillsByFilters

urlpatterns = [
    path('', TransactionsListView.as_view(), name='transactions_list'),
    path('<int:id>', OneTransactionView.as_view(), name='one_transaction'),
    path('CA/', RevenuesAndBillsByFilters.as_view(), name='revenue_by_filters')
]
