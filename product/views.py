import json
from datetime import datetime

from django.http import JsonResponse, Http404
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product
from product.serializer import ProductSerializer
from transaction.serializer import TransactionSerializer


class GetProducts:

    @staticmethod
    def get_product(tig_id) -> Product:
        try:
            return Product.objects.get(tig_id=tig_id)
        except Product.DoesNotExist:
            raise Http404


class GetJsons:

    @staticmethod
    def get_jsons(body) -> json:
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError:
            raise Http404


class CreateTransaction:
    @staticmethod
    def create_transaction(product: Product, body) -> TransactionSerializer:
        transaction_quantity = body['quantityInStock'] -product.quantityInStock

        if transaction_quantity < 0 and body['purchasePrice'] == 0:
            transaction_type = 'retraitInvendus'
        elif transaction_quantity < 0 < body['purchasePrice']:
            transaction_type = 'retraitVente'
        else:
            transaction_type = 'ajout'

        return TransactionSerializer(
            data={"date": datetime.now(),
                  "tig_id": body['tig_id'],
                  "category": product.category,
                  "quantity": transaction_quantity,
                  "price": body['purchasePrice'],
                  "onSale": body['sale'],
                  "type": transaction_type
                  })


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request) -> JsonResponse:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({
            'success': True,
            'products': serializer.data
        }, status=200)


class OneProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tig_id) -> JsonResponse:
        product = GetProducts.get_product(tig_id)
        serializer = ProductSerializer(product)
        return JsonResponse({
            'success': True,
            'product': serializer.data
        }, status=200)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, tig_id) -> JsonResponse:
        product = GetProducts.get_product(tig_id)
        serializer = ProductSerializer(product, data=GetJsons.get_jsons(request.body), partial=True)
        transaction_serializer = CreateTransaction.create_transaction(product, GetJsons.get_jsons(request.body))
        if serializer.is_valid(raise_exception=True) and transaction_serializer.is_valid(raise_exception=True):
            serializer.save()
            transaction_serializer.save()
            return JsonResponse({
                'success': True,
                'product': serializer.data
            }, status=201)
        return JsonResponse({
            "success": False
        })


class UpdateMultipleProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request) -> JsonResponse:
        try:
            return_array = []

            for product_data in GetJsons.get_jsons(request.body):
                tig_id = product_data.get('tig_id')
                if not tig_id:
                    continue

                # Récupérer le produit à mettre à jour
                product = GetProducts.get_product(tig_id)

                # Sérialiser et valider les données
                serializer = ProductSerializer(product, data=product_data, partial=True)
                transaction_serializer = CreateTransaction.create_transaction(product, GetJsons.get_jsons(request.body))
                if serializer.is_valid(raise_exception=True) and transaction_serializer.is_valid(raise_exception=True):
                    serializer.save()
                    transaction_serializer.save()
                    return_array.append(serializer.data)

            return JsonResponse({
                'success': True,
                'products': return_array
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Http404:
            return JsonResponse({'error': 'Product not found.'}, status=404)
