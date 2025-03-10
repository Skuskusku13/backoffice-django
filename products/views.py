import json

from django.http import JsonResponse, Http404
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.models import Products
from products.serializer import ProductSerializer

class GetProducts:

    @staticmethod
    def get_product(tig_id) -> Products:
        try:
            return Products.objects.get(tig_id=tig_id)
        except Products.DoesNotExist:
            raise Http404

class GetJsons:

    @staticmethod
    def get_jsons(body) -> json:
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError:
            raise Http404

class ProductListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request) -> JsonResponse:
        products = Products.objects.all()
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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return_array.append(serializer.data)

            return JsonResponse({
                'success': True,
                'products': return_array
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Http404:
            return JsonResponse({'error': 'Product not found.'}, status=404)
