import json

from django.http import JsonResponse, Http404
from django.views import View
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

class ProductListView(View):

    def get(self, request) -> JsonResponse:
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({
            'success': True,
            'product': serializer.data
        }, status=200)


class OneProductView(View):

    def get(self, request, tig_id) -> JsonResponse:
        product = GetProducts.get_product(tig_id)
        serializer = ProductSerializer(product)
        return JsonResponse({
            'success': True,
            'product': serializer.data
        }, status=200)

class UpdateProductView(View):

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