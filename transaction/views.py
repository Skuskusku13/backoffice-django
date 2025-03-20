from datetime import timedelta, datetime

from django.db.models import Sum
from django.http import JsonResponse, Http404
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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


class RevenuesAndBillsByFilters(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupération des filtres
        period = request.GET.get('period', 'year')
        sale_type = request.GET.get('type', 'all')
        category = request.GET.get('category', None)
        transactions = Transaction.objects

        # Filtre par catégorie
        if category:
            transactions = transactions.filter(category=category)
        # Filtre par promo
        if sale_type == "true":
            transactions = transactions.filter(onSale=True)
        elif sale_type == "false":
            transactions = transactions.filter(onSale=False)

        # Filtre par période avec %% pour échapper le %
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if period == 'year':
            start_date = today.replace(month=1, day=1)
            date_format = "%%Y"
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
            date_format = "%%Y-Q%%m"
        elif period == 'month':
            start_date = today.replace(day=1)
            date_format = "%%Y-%%m"
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            date_format = "%%Y-%%W"
        else:
            start_date = today
            date_format = "%%Y-%%m-%%d"
        transactions_by_start_date = transactions.filter(date__gte=start_date)

        transactions_ventes_actual = transactions_by_start_date.filter(type="retraitVente")
        transactions_ajouts_actual = transactions_by_start_date.filter(type="ajout")
        transactions_ventes = transactions.filter(type="retraitVente")
        transactions_ajouts = transactions.filter(type="ajout")

        total_revenue_actual = sum([t.get_price() for t in transactions_ventes_actual])
        total_revenue = sum([t.get_price() for t in transactions_ventes])
        revenues_by_period = (
            transactions_ventes
            .extra(select={'date_group': f"strftime('{date_format}', date)"})
            .values('date_group')
            .annotate(total=Sum('price'))
            .order_by('date_group')
        )
        total_bills_actual = sum([t.get_price() for t in transactions_ajouts_actual])
        total_bills = sum([t.get_price() for t in transactions_ajouts])
        bills_by_period = (
            transactions_ajouts
            .extra(select={'date_group': f"strftime('{date_format}', date)"})
            .values('date_group')
            .annotate(total=Sum('price'))
            .order_by('date_group')
        )

        return Response({
            "totalRevenueActual": total_revenue_actual,
            "totalRevenue": total_revenue,
            "revenuesByPeriod": list(revenues_by_period),
            "totalBillsActual": total_bills_actual,
            "totalBills": total_bills,
            "billsByPeriod": list(bills_by_period)
        })
