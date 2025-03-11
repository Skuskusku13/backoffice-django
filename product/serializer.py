from rest_framework.serializers import ModelSerializer
from product.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'tig_id',
            'name',
            'category',
            'price',
            'unit',
            'availability',
            'sale',
            'discount',
            'comments',
            'owner',
            'quantityInStock'
        )
