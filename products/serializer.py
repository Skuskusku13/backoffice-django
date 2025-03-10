from rest_framework.serializers import ModelSerializer
from products.models import Products

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
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
