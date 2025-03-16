from xmlrpc.client import DateTime

from django.core.management.base import BaseCommand, CommandError
import requests
import time

from transaction.models import Transaction
from transaction.serializer import TransactionSerializer


class Command(BaseCommand):
    help = 'Add first transactions in database'

    def handle(self, *args, **options):
        self.stdout.write('[' + time.ctime() + '] Adding data...')
        Transaction.objects.all().delete()
        data = [{
            'tig_id': '12',
            'quantity': '27',
            'price': 8.2,
        },{
            'tig_id': '12',
            'quantity': '11',
            'price': 2,
        },{
            'tig_id': '12',
            'quantity': '12',
            'price': 3.1,
        }]
        for transaction in data:
            serializer = TransactionSerializer(data={
                'tig_id': str(transaction['tig_id']),
                'quantity': str(transaction['quantity']),
                'price': str(transaction['price']),
            })
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(
                    self.style.SUCCESS('[' + time.ctime() + '] Successfully added transaction'))

        self.stdout.write('[' + time.ctime() + '] Data add terminated.')
