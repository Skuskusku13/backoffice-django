from datetime import timedelta

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


class RevenueByFilters(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupération des filtres
        period = request.GET.get('period', 'year')
        sale_type = request.GET.get('type', 'all')
        category = request.GET.get('category', None)

        # Filtre par catégorie
        transactions = Transaction.objects.filter(type="retraitVente")
        if category:
            transactions = transactions.filter(category=category)
        # Filtre par promo
        if sale_type == "true":
            transactions = transactions.filter(onSale=True)
        elif sale_type == "false":
            transactions = transactions.filter(onSale=False)
        # Filtre par période avec %% pour échapper le %
        today = now()
        if period == 'year':
            start_date = today.replace(month=1, day=1)
            date_format = "%%Y"
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
            date_format = "%%Y-%%m"
        elif period == 'month':
            start_date = today.replace(day=1)
            date_format = "%%Y-%%m"
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            date_format = "%%Y-%%m-%%d"
        else:
            start_date = today
            date_format = "%%Y-%%m-%%d"

        # Filtrage par start_date
        transactions = transactions.filter(date__gte=start_date)
        # Calcul du chiffre d'affaires total
        total_revenue = sum([t.get_revenue() for t in transactions])
        # Préparation des données pour le graphique (groupées par date)
        revenue_per_period = (
            transactions
            .extra(select={'date_group': f"strftime('{date_format}', date)"})
            .values('date_group')
            .annotate(total=Sum('price'))
            .order_by('date_group')
        )

        return Response({
            "total_revenue": total_revenue,
            "revenue_per_period": list(revenue_per_period)
        })


class RevenuesByFilters(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupération des filtres
        period = request.GET.get('period', 'year')
        sale_type = request.GET.get('type', 'all')
        category = request.GET.get('category', None)

        # Filtre par catégorie
        transactions = Transaction.objects.filter(type="retraitVente")
        if category:
            transactions = transactions.filter(category=category)
        # Filtre par promo
        if sale_type == "true":
            transactions = transactions.filter(onSale=True)
        elif sale_type == "false":
            transactions = transactions.filter(onSale=False)

        # Définir la première transaction comme point de départ
        # first_transaction = transactions.order_by('date').first()
        # if not first_transaction:
        #     return Response({"total_revenue": 0, "revenue_per_period": []})
        # start_date = first_transaction.date
        # today = now()

        # Filtre par période avec %% pour échapper le %
        if period == 'year':
            # start_date = today.replace(month=1, day=1)
            date_format = "%%Y"
        elif period == 'quarter':
            date_format = "%%Y-Q %%m/3+1"
        elif period == 'month':
            date_format = "%%Y-%%m"
        elif period == 'week':
            date_format = "%%Y-%%W"
        else:
            date_format = "%%Y-%%m-%%d"

        # Filtrage par start_date
        # transactions = transactions.filter(date__gte=start_date)
        # Calcul du chiffre d'affaires total
        total_revenue = sum([t.get_revenue() for t in transactions])
        # Préparation des données pour le graphique (groupées par date)
        revenue_per_period = (
            transactions
            .extra(select={'date_group': f"strftime('{date_format}', date)"})
            .values('date_group')
            .annotate(total=Sum('price'))
            .order_by('date_group')
        )

        return Response({
            "total_revenue": total_revenue,
            "revenue_per_period": list(revenue_per_period)
        })
