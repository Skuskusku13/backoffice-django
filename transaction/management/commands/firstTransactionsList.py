import json
import os
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

        file_path = os.path.join(os.path.dirname(__file__), 'transactions.json')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File 'transactions.json' not found."))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format."))
            return
        i = 1
        for transaction in data:
            serializer = TransactionSerializer(data={
                'date': str(transaction['date']),
                'tig_id': str(transaction['tig_id']),
                'category': str(transaction['category']),
                'quantity': str(transaction['quantity']),
                'price': str(transaction['price']),
                'onSale': str(transaction['onSale']),
                'type': str(transaction['type']),
            })
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(
                    self.style.SUCCESS('[' + time.ctime() + '] Successfully added transaction ' + str(i)))
                i += 1

        self.stdout.write('[' + time.ctime() + '] Data add terminated.')
