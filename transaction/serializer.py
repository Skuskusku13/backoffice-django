from rest_framework.serializers import ModelSerializer

from transaction.models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'date',
            'tig_id',
            'category',
            'quantity',
            'price',
            'onSale',
            'type'
        )
