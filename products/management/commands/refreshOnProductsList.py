from django.core.management.base import BaseCommand, CommandError
from products.models import Products
from products.serializer import ProductSerializer
from products.config import URL_BINH
import requests
import time


class Command(BaseCommand):
    help = 'Refresh the list of products from TiG server.'

    def handle(self, *args, **options):
        self.stdout.write('[' + time.ctime() + '] Refreshing data...')
        response = requests.get(URL_BINH + 'products/')
        jsondata = response.json()
        Products.objects.all().delete()
        for product in jsondata:
            serializer = ProductSerializer(data={
                'tig_id':       str(product['id']),
                'name':         str(product['name']),
                'category':     str(product['category']),
                'price':        str(product['price']),
                'unit':         str(product['unit']),
                'availability': str(product['availability']),
                'sale':         str(product['sale']),
                'discount':     str(product['discount']),
                'comments':     str(product['comments']),
                'owner':        str(product['owner']),
                'quantityInStock': '0',
            })
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(
                    self.style.SUCCESS('[' + time.ctime() + '] Successfully added product id="%s"' % product['id']))
        self.stdout.write('[' + time.ctime() + '] Data refresh terminated.')
