from django.http import JsonResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from transaction.models import Transaction
from transaction.serializer import TransactionSerializer


# Create your views here.
class TransactionsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request) -> JsonResponse:
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse({
            'success': True,
            'transactions': serializer.data
        }, status=200)


class OneTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id) -> JsonResponse:
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            raise Http404
        serializer = TransactionSerializer(transaction)
        return JsonResponse({
            'success': True,
            'transaction': serializer.data
        }, status=200)
